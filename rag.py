import re
import numpy
import loaders
import ux
import difflib


def search_results(query, top_k=5, context_window=1):
    query_embedding = loaders.sentence_model.encode([query])
    normalized_query = query_embedding / numpy.linalg.norm(query_embedding)  # type: ignore
    _, I = loaders.search_index.search(normalized_query, top_k)  # type: ignore
    results = [loaders.dataframe.iloc[idx] for idx in I[0]]

    contextualized_results = []
    for result in results:
        book, chapter, verse = (
            result["book"],
            int(result["chapter"]),
            int(result["verse"]),
        )

        # Get surrounding verses
        context_verses = loaders.dataframe[
            (loaders.dataframe["book"] == book)
            & (loaders.dataframe["chapter"].astype(int) == chapter)
            & (
                loaders.dataframe["verse"]
                .astype(int)
                .between(verse - context_window, verse + context_window)
            )
        ]

        # Sort verses to ensure correct order
        context_verses = context_verses.sort_values("verse")  # type: ignore

        # Combine verses into a single string
        combined_text = " ".join(context_verses["passage"])

        # Create a new result with both original and combined text
        contextualized_result = result.copy()
        contextualized_result["contextualized_passage"] = combined_text
        contextualized_results.append(contextualized_result)

    return contextualized_results


def results_citations(results):
    return [
        f"{result['book']} {result['chapter']}:{result['verse']} - {result['passage']}"
        for result in results
    ]


def generate_answers(query, results):
    answers = []
    max_len = ux._get_term_width() - 8
    for result in results:
        # input_text = f"question: {query}\n\ncontext: {result['contextualized_passage']}"
        instructions = f"Using the context provided containing a passage from the Book of Mormon, answer the following question in full sentences."
        input_text = f"{instructions}\n\nquestion: {query}\n\ncontext: {result['contextualized_passage']}:"
        input_ids = loaders.tokenizer.encode(input_text, return_tensors="pt")
        outputs = loaders.answer_model.generate(
            input_ids,  # type: ignore
            max_length=150,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        answer = loaders.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if makes_sense_enough(f"{answer}", instructions):
            answer_text = f"{answer}"
            answer_text = (
                answer_text
                if len(answer_text) <= max_len
                else f"{answer_text[:max_len]}..."
            )
            print(ux.info(f"·> ({answer_text})"))
            answers.append(
                {
                    "answer": answer,
                    "result": result,
                }
            )
    return answers


def summarize_answers(answers, query, _):
    concatenated_answer = " ".join(
        [
            f"""In chapter {a['result']['chapter']}, verse {a['result']['verse']}, {a['result']['book']} wrote, "{a['result']['passage']}". This means that {a['answer']}."""
            for a in answers
        ]
    )

    prompt = f"""{query}\n\n{concatenated_answer}"""
    return loaders.summarization_model(  # type: ignore
        prompt,
        min_new_tokens=12,
        max_new_tokens=120,
        do_sample=False,
    )[0]["summary_text"]


def makes_sense_enough(text, prompt, max_similarity_ratio=0.7):
    text = text.lower()
    text_words = re.findall(r"\b\w+\b", text)

    prompt = prompt.lower()
    prompt_words = re.findall(r"\b\w+\b", prompt)

    # Check if all text_words are in prompt_words
    if all(word in prompt_words for word in text_words):
        return False

    # Check similarity to prompt
    similarity_ratio = difflib.SequenceMatcher(None, text, prompt).ratio()
    if similarity_ratio > max_similarity_ratio:
        return False

    return True
