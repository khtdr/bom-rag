install:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/pip3 install pandas faiss-cpu transformers sentence-transformers torch sentencepiece
	./venv/bin/python3 main.py --help 2>warnings.log

build: install
	./venv/bin/python3 main.py --build 2>warnings.log

run:
	./venv/bin/python3 main.py 2>warnings.log

run-ssh:
	scp *.py joey@192.168.0.68:~/opt/bom-rag/
	ssh -t joey@192.168.0.68 'cd ~/opt/bom-rag/ && make run'

.PHONY: install build run run-ssh
.SILENT: install build run
