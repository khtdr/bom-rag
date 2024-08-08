import os
import re
import argparse
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

parser = argparse.ArgumentParser(description='RAG CLI for "ThE bOoK oF mOrMoN"')
parser.add_argument('--build', action='store_true', help='Build the embeddings and FAISS index files')
args = parser.parse_args()

# File paths
embeddings_file = 'embeddings.npy'
faiss_index_file = 'faiss_index.bin'


# Load and process lines
data = []
pattern = r'^(.*)\s(\d+):(\d+)\s{5}(.*)$'
with open('./bom.txt') as file:
    while line := file.readline():
        if not line.strip(): break
        book, chapter, verse, passage = re.search(pattern, line).groups()
        data.append({ 'book': book, 'chapter':chapter, 'verse':verse, 'passage':passage})

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Check if we need to rebuild embeddings and FAISS index
if args.rebuild or not os.path.exists(embeddings_file) or not os.path.exists(faiss_index_file):
    print("Building embeddings and FAISS index...")

    # Create embeddings for each passage
    df['embedding'] = df['passage'].apply(lambda x: model.encode(x))
    np.save(embeddings_file, df['embedding'].tolist())

    # Load embeddings
    embeddings = np.load(embeddings_file)

    # Build the FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    faiss.write_index(index, faiss_index_file)
else:
    print("Loading existing embeddings and FAISS index...")

    # Load embeddings
    embeddings = np.load(embeddings_file)

    # Load the FAISS index
    index = faiss.read_index(faiss_index_file)

# Load QA model
qa_model = pipeline('question-answering', model='deepset/roberta-base-squad2')

def search(query, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype=np.float32), top_k)

    results = []
    for idx in I[0]:
        results.append(df.iloc[idx])

    return results

def generate_answer(query):
    results = search(query)

    # Use QA model to answer the question based on retrieved passages
    answers = []
    for result in results:
        answer = qa_model(question=query, context=result['passage'])
        answers.append({
            'answer': answer['answer'],
            'score': answer['score'],  # Save the score to sort later
            'citation': f"{result['book']} {result['chapter']}:{result['verse']}\n{result['passage']}"
        })

    # Sort answers by the confidence score in descending order
    answers = sorted(answers, key=lambda x: x['score'], reverse=True)

    return answers

def answer_query(query):
    answers = generate_answer(query)

    print("Answers and Citations (Sorted by Best Answer):")
    for i, answer_data in enumerate(answers):
        print(f"\nAnswer {i+1}:")
        print(answer_data['answer'])
        print("Citation:")
        print(answer_data['citation'])

# Example usage
answer_query("When is self defense justifiable?")
