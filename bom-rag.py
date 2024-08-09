import os
import re
import argparse
import pandas
import numpy
import torch
import faiss
import transformers
from sentence_transformers import SentenceTransformer

# important files
bom_source_file = 'bom.txt'
passages_file = 'passages.json'
embeddings_file = 'embeddings.npy'
faiss_index_file = 'faiss_index.bin'

# usage and options
parser = argparse.ArgumentParser(description='RAG CLI for "ThE bOoK oF mOrMoN"')
parser.add_argument('--build', action='store_true', help='Build the embeddings and FAISS index files')
args = parser.parse_args()

# read and/or create the passages json file into a DataFrame
if args.build or not os.path.exists(passages_file):
    data = []
    pattern = r'^(.*)\s(\d+):(\d+)\s{5}(.*)$'
    with open(bom_source_file) as file:
        while line := file.readline():
            if not line.strip(): continue
            book, chapter, verse, passage = re.search(pattern, line).groups()
            data.append({ 'book':book, 'chapter':chapter, 'verse':verse, 'passage':passage})
    df = pandas.DataFrame(data)
    df.to_json(passages_file, orient='records')
else:
    data = []
    with open(passages_file, 'r') as file:
        data = pandas.read_json(file).to_dict('records')
    df = pandas.DataFrame(data)

# the sentence model used...
model = SentenceTransformer('all-MiniLM-L6-v2')

# read and/or create the embeddings file
if args.build or not os.path.exists(embeddings_file):
    df['embedding'] = df['passage'].apply(lambda x: model.encode(x))
    numpy.save(embeddings_file, df['embedding'].tolist())
    embeddings = numpy.load(embeddings_file)
else:
    embeddings = numpy.load(embeddings_file)

# read and/or create the faiss index file
if args.build or not os.path.exists(embeddings_file) or not os.path.exists(faiss_index_file):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(numpy.array(embeddings, dtype=numpy.float32))
    faiss.write_index(index, faiss_index_file)
else:
    index = faiss.read_index(faiss_index_file)

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1

# use a model good for Q/A
qa_model = transformers.pipeline('question-answering', model='deepset/roberta-base-squad2', device=device)

def search(query, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(numpy.array(query_embedding, dtype=numpy.float32), top_k)
    results = []
    for idx in I[0]:
        results.append(df.iloc[idx])
    return results

def generate_answer(query):
    results = search(query)
    answers = []
    for result in results:
        answer = qa_model(question=query, context=result['passage'])
        answers.append({
            'answer': answer['answer'],
            'score': answer['score'],  # Save the score to sort later
            'citation': f"{result['book']} {result['chapter']}:{result['verse']}\n{result['passage']}"
        })
    answers = sorted(answers, key=lambda x: x['score'], reverse=True)
    return answers


from transformers import T5ForConditionalGeneration, T5Tokenizer
# Using T5 for Question Answering
model_name = "t5-large"  # or "t5-3b" for even better performance
t5_tokenizer = T5Tokenizer.from_pretrained(model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_answer_with_t5(query):
    results = search(query)
    answers = []
    for result in results:
        # Use the T5 model to generate answers
        # answer = generate_answer_with_t5(query, result['passage'])
        input_text = f"question: {query} context: {result['passage']}"
        input_ids = t5_tokenizer.encode(input_text, return_tensors='pt')
        outputs = t5_model.generate(input_ids)
        answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        answers.append({
            'answer': answer,
            'citation': f"{result['book']} {result['chapter']}:{result['verse']}\n{result['passage']}"
        })
    return answers

def answer_query(query):
    # answers = generate_answer(query)
    # print("Answers and Citations (Sorted by Best Answer):")
    # for i, answer_data in enumerate(answers):
    #     print(f"\nAnswer {i+1}:")
    #     print(answer_data['answer'])
    #     print("Citation:")
    #     print(answer_data['citation'])
    answers = generate_answer_with_t5(query)
    print("Answers and Citations (T5) (Sorted by Best Answer):")
    for i, answer_data in enumerate(answers):
        print(f"\nAnswer {i+1}:")
        print(answer_data['answer'])
        print("Citation:")
        print(answer_data['citation'])

answer_query("When is self-defense justifiable?")
