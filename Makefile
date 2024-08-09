
install:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/pip3 install pandas faiss-cpu transformers sentence-transformers torch sentencepiece
	./venv/bin/python3 bom-rag.py --help 2>warnings.log

build: install
	./venv/bin/python3 bom-rag.py --build 2>warnings.log

run:
	./venv/bin/python3 bom-rag.py 2>warnings.log

.PHONY: install build run
.SILENT: install build run
