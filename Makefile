
install:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/pip3 install pandas faiss-cpu transformers sentence-transformers
	./venv/bin/python3 bom-rag.py --help

build: install
	./venv/bin/python3 bom-rag.py --build

run:
	./venv/bin/python3 bom-rag.py

.PHONY: install build run
