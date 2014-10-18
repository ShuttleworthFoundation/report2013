PHONY: default build pull

default: pull build

pull:
	git submodule update --init --recursive
	git submodule foreach --recursive git pull

build: venv
	. venv/bin/activate && src/scripts/generate.py

venv: venv/bin/activate venv/.updated

venv/bin/activate:
	virtualenv venv

venv/.updated: src/requirements.txt
	. venv/bin/activate && pip install -r src/requirements.txt
	touch $@
