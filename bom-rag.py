import os
import re
import argparse
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

# Set up CLI argument parsing
parser = argparse.ArgumentParser(description='RAG System for a "ThE bOoK oF mOrMoN"')
parser.add_argument('--rebuild', action='store_true', help='Rebuild the embeddings and FAISS index')
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

# Load summarization pipeline
summarizer = pipeline('summarization')

def search(query, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype=np.float32), top_k)

    results = []
    for idx in I[0]:
        results.append(df.iloc[idx])

    return results

def generate_answer(query):
    results = search(query)

    # Combine passages from the search results
    passages = " ".join([result['passage'] for result in results])

    # Generate summary
    summary = summarizer(passages, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

    # Add citations
    citations = []
    for result in results:
        citations.append(f"{result['book']} {result['chapter']}:{result['verse']}\n{result['passage']}")

    return summary, citations

def answer_query(query):
    summary, citations = generate_answer(query)
    print("Summary:")
    print(summary)
    print("\nCitations:")
    for citation in citations:
        print(citation)

# Example usage
answer_query("infant baptism")
