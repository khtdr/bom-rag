install:
	python -m venv venv
	./venv/bin/pip install pandas faiss-cpu transformers sentence-transformers
	./venv/bin/python bom-rag.py --help

build: install
	./venv/bin/python bom-rag.py --build

run:
	./venv/bin/python bom-rag.py

.PHONY install build run
