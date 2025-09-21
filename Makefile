SHELL = /bin/bash

build:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt

test:
	source .venv/bin/activate && \
	pytest 

format:
	source .venv/bin/activate && \
	black .

lint:
	source .venv/bin/activate && \
	pylint .