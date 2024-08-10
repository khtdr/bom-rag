install:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/pip3 install pandas faiss-cpu transformers sentence-transformers torch sentencepiece colorama
	./venv/bin/python3 bom-rag.py --help 2>warnings.log

build: install
	./venv/bin/python3 bom-rag.py --build 2>warnings.log

run:
	./venv/bin/python3 bom-rag.py 2>warnings.log

run-ssh:
	scp bom-rag.py joey@192.168.0.68:~/opt/bom-rag/bom-rag.py
	ssh -t joey@192.168.0.68 'cd ~/opt/bom-rag/ && make run'

.PHONY: install build run run-ssh
.SILENT: install build run
