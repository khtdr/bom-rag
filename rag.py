import numpy
import loaders


def search_results(query, top_k=5):
    query_embedding = loaders.sentence_model.encode([query])
    normalized_query = query_embedding / numpy.linalg.norm(query_embedding)  # type: ignore
    _, I = loaders.search_index.search(normalized_query, top_k)  # type: ignore
    results = [loaders.dataframe.iloc[idx] for idx in I[0]]

    # Add context by including neighboring verses
    contextualized_results = []
    for result in results:
        book, chapter, verse = (
            result["book"],
            int(result["chapter"]),
            int(result["verse"]),
        )
        context = loaders.dataframe[
            (loaders.dataframe["book"] == book)
            & (loaders.dataframe["chapter"].astype(int) == chapter)
            & (loaders.dataframe["verse"].astype(int).between(verse - 1, verse + 2))
        ]
        contextualized_results.extend(context.to_dict("records"))  # type: ignore

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for item in contextualized_results:
        item_tuple = tuple(item.items())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_results.append(item)

    return unique_results[:top_k]


def generate_answers_with_t5(query, results):
    answers = []
    for result in results:
        input_text = f"Using the context provided containing a passage from the Book of Mormon, answer the following question using full sentences in an accurate and direct tone of voice.\n\nquestion: {query}\n\ncontext: {result['passage']}:"
        input_ids = loaders.tokenizer.encode(input_text, return_tensors="pt")
        outputs = loaders.t5_model.generate(
            input_ids,  # type: ignore
            max_length=150,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        answer = loaders.tokenizer.decode(outputs[0], skip_special_tokens=True)
        scored_answer = loaders.qa_model(question=query, context=result["passage"])  # type: ignore
        answers.append(
            {
                "answer": answer,
                "result": result,
                "score": scored_answer["score"],
            }
        )
    return sorted(answers, key=lambda x: x["score"], reverse=True)


def get_citations(results):
    return [
        f"{result['book']} {result['chapter']}:{result['verse']} - {result['passage']}"
        for result in results
    ]


def generate_summarized_answer(answers):
    concatenated_answer = " ".join([answer_data["answer"] for answer_data in answers])
    return loaders.summarization_model(  # type: ignore
        concatenated_answer, max_length=150, min_length=30, do_sample=False
    )[0]["summary_text"]
