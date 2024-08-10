import os
import re
import argparse
import pandas as pd
import numpy as np
import torch
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

# Important files
BOM_SOURCE_FILE = "bom.txt"
PASSAGES_FILE = "passages.json"
EMBEDDINGS_FILE = "embeddings.npy"
FAISS_INDEX_FILE = "faiss_index.bin"

# Models
MODEL_NAME = "t5-large"
SENTENCE_MODEL = "all-mpnet-base-v2"  # 'all-MiniLM-L6-v2'
QA_MODEL = "deepset/roberta-base-squad2"
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"


def parse_arguments():
    parser = argparse.ArgumentParser(description='RAG CLI for "ThE bOoK oF mOrMoN"')
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the embeddings and FAISS index files",
    )
    return parser.parse_args()


def load_or_create_passages(build):
    if build or not os.path.exists(PASSAGES_FILE):
        data = []
        pattern = r"^(.*)\s(\d+):(\d+)\s{5}(.*)$"
        with open(BOM_SOURCE_FILE) as file:
            for line in file:
                if line.strip():
                    book, chapter, verse, passage = re.search(pattern, line).groups()
                    data.append(
                        {
                            "book": book,
                            "chapter": chapter,
                            "verse": verse,
                            "passage": passage,
                        }
                    )
        df = pd.DataFrame(data)
        df.to_json(PASSAGES_FILE, orient="records")
    else:
        df = pd.read_json(PASSAGES_FILE)
    return df


def load_or_create_embeddings(df, model, build):
    if build or not os.path.exists(EMBEDDINGS_FILE):
        print("Creating embeddings...")
        df["embedding"] = df["passage"].apply(lambda x: model.encode(x))
        np.save(EMBEDDINGS_FILE, df["embedding"].tolist())
    return np.load(EMBEDDINGS_FILE)


def load_or_create_faiss_index(embeddings, build):
    if (
        build
        or not os.path.exists(EMBEDDINGS_FILE)
        or not os.path.exists(FAISS_INDEX_FILE)
    ):
        print("Creating FAISS index...")
        index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )  # Changed to IndexFlatIP for cosine similarity
        normalized_embeddings = (
            embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        )
        index.add(normalized_embeddings)
        faiss.write_index(index, FAISS_INDEX_FILE)
    else:
        index = faiss.read_index(FAISS_INDEX_FILE)
    return index


def improved_search(query, index, df, model, top_k=5):
    query_embedding = model.encode([query])
    normalized_query = query_embedding / np.linalg.norm(query_embedding)
    D, I = index.search(normalized_query, top_k)
    results = [df.iloc[idx] for idx in I[0]]

    # Add context by including neighboring verses
    contextualized_results = []
    for result in results:
        book, chapter, verse = (
            result["book"],
            int(result["chapter"]),
            int(result["verse"]),
        )
        context = df[
            (df["book"] == book)
            & (df["chapter"].astype(int) == chapter)
            & (df["verse"].astype(int).between(verse - 1, verse + 1))
        ]
        contextualized_results.extend(context.to_dict("records"))

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for item in contextualized_results:
        item_tuple = tuple(item.items())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_results.append(item)

    return unique_results[:top_k]


def generate_answer_with_t5(query, results, t5_tokenizer, t5_model, qa_model):
    answers = []
    for result in results:
        input_text = f"question: {query} context: {result['passage']}"
        input_ids = t5_tokenizer.encode(input_text, return_tensors="pt")
        outputs = t5_model.generate(input_ids)
        answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        scored_answer = qa_model(question=query, context=result["passage"])
        answers.append(
            {
                "answer": answer,
                "score": scored_answer["score"],
                "citation": f"{result['book']} {result['chapter']}:{result['verse']} -\n{result['passage']}",
            }
        )
    return sorted(answers, key=lambda x: x["score"], reverse=True)


def generate_summarized_answer(
    query, results, t5_tokenizer, t5_model, qa_model, summarization_model
):
    answers = generate_answer_with_t5(query, results, t5_tokenizer, t5_model, qa_model)
    concatenated_answer = " ".join([answer_data["answer"] for answer_data in answers])
    summarized_answer = summarization_model(
        concatenated_answer, max_length=150, min_length=30, do_sample=False
    )[0]["summary_text"]
    citations = "\n\n".join([f"{answer_data['citation']}" for answer_data in answers])
    return f"{summarized_answer}\n{citations}\n\n"


def main():
    args = parse_arguments()

    # Load models and data
    sentence_model = SentenceTransformer(SENTENCE_MODEL)
    df = load_or_create_passages(args.build)
    embeddings = load_or_create_embeddings(df, sentence_model, args.build)
    index = load_or_create_faiss_index(embeddings, args.build)

    if args.build:
        print("Setup is done.")
    else:
        device = 0 if torch.cuda.is_available() else -1
        qa_model = pipeline("question-answering", model=QA_MODEL, device=device)
        summarization_model = pipeline("summarization", model=SUMMARIZATION_MODEL)
        t5_tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
        t5_model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

        print("bOoK oF mOrMoN RAG ready. Type your questions or press Ctrl+D to exit.")
        print("----------------------------------------------------------------------")
        while True:
            try:
                print("What is your question? (Ctrl+D to exit)")
                print(">", end=" ")
                query = input()
                if not query.strip():
                    continue
                print("sEaRcHiNg FoR aNsWeRs...")
                results = improved_search(query, index, df, sentence_model)
                final_answer = generate_summarized_answer(
                    query,
                    results,
                    t5_tokenizer,
                    t5_model,
                    qa_model,
                    summarization_model,
                )
                print(final_answer)
            except EOFError:
                print("\nuNtIl We mEeT aGaIn")
                break


if __name__ == "__main__":
    main()
