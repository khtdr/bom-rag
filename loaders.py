from typing import Any
import faiss
import numpy
import os
import pandas
import re
import sentence_transformers
import transformers
import torch


# Paths to required asset files
_BOM_SOURCE_FILE = "bom.txt"
_PASSAGES_FILE = "passages.json"
_EMBEDDINGS_FILE = "embeddings.npy"
_FAISS_INDEX_FILE = "faiss_index.bin"


# Models by name being used
_MODEL_NAME = "t5-large"
_SENTENCE_MODEL = "all-mpnet-base-v2"
_QA_MODEL = "deepset/roberta-base-squad2"
_SUMMARIZATION_MODEL = "facebook/bart-large-cnn"


# Assets, models, tokenizers, etc. that are used in the RAG
_device = 0 if torch.cuda.is_available() else -1
dataframe: pandas.DataFrame = None  # type: ignore
embeddings: Any = None  # type: ignore
search_index: faiss.IndexFlatIP = None  # type: ignore
sentence_model: sentence_transformers.SentenceTransformer = None  # type: ignore
qa_model: transformers.Pipeline = None  # type: ignore
summarization_model: transformers.Pipeline = None  # type: ignore
tokenizer: transformers.T5Tokenizer = None  # type: ignore
answer_model: transformers.T5ForConditionalGeneration = None  # type: ignore


def load_or_create_models():
    global sentence_model, qa_model, summarization_model, answer_model, tokenizer
    sentence_model = sentence_model or sentence_transformers.SentenceTransformer(
        _SENTENCE_MODEL
    )
    qa_model = qa_model or transformers.pipeline(
        "question-answering", model=_QA_MODEL, device=_device
    )
    summarization_model = summarization_model or transformers.pipeline(
        "summarization", model=_SUMMARIZATION_MODEL, device=_device
    )
    tokenizer = tokenizer or transformers.T5Tokenizer.from_pretrained(_MODEL_NAME)
    answer_model = (
        answer_model
        or transformers.T5ForConditionalGeneration.from_pretrained(_MODEL_NAME)
    )


def load_or_create_assets(build=False):
    """Ensures the required files are built and returns their assets"""
    global dataframe, embeddings, search_index
    dataframe = _load_or_create_dataframe(build)
    embeddings = embeddings or _load_or_create_embeddings(dataframe, build)
    search_index = search_index or _load_or_create_search_index(embeddings, build)
    return [dataframe, search_index]


def _load_or_create_dataframe(build=False):
    """Parses the BoM input text and creates a dataframe of passages"""
    if build or not os.path.exists(_PASSAGES_FILE):
        data = []
        pattern = r"^(.*)\s(\d+):(\d+)\s{5}(.*)$"
        with open(_BOM_SOURCE_FILE) as file:
            for line in file:
                if line.strip():
                    match = re.search(pattern, line)
                    if match:
                        book, chapter, verse, passage = match.groups()
                        data.append(
                            {
                                "book": book,
                                "chapter": chapter,
                                "verse": verse,
                                "passage": passage,
                            }
                        )
        dataframe = pandas.DataFrame(data)
        dataframe.to_json(_PASSAGES_FILE, orient="records")
    else:
        dataframe = pandas.read_json(_PASSAGES_FILE)
    return dataframe


def _load_or_create_embeddings(dataframe, build=False):
    """Creates vector embeddings for the passages in the dataframe"""
    load_or_create_models()
    if build or not os.path.exists(_EMBEDDINGS_FILE):
        dataframe["embedding"] = dataframe["passage"].apply(
            lambda x: sentence_model.encode(x)
        )
        numpy.save(_EMBEDDINGS_FILE, dataframe["embedding"].tolist())
    return numpy.load(_EMBEDDINGS_FILE)


def _load_or_create_search_index(embeddings, build=False):
    """Creates a FAISS index file for the given embeddings, using cosine similarity"""
    if (
        build
        or not os.path.exists(_EMBEDDINGS_FILE)
        or not os.path.exists(_FAISS_INDEX_FILE)
    ):
        index = faiss.IndexFlatIP(embeddings.shape[1])
        vector_length = numpy.linalg.norm(embeddings, axis=1)
        normalized_embeddings = embeddings / vector_length[:, numpy.newaxis]
        index.add(normalized_embeddings)  # type: ignore (bad type info)
        faiss.write_index(index, _FAISS_INDEX_FILE)
    else:
        index = faiss.read_index(_FAISS_INDEX_FILE)
    return index
