.PHONY: default build update help

default: build

help:
	@echo 'Available targets:'
	@echo
	@echo 'help - Show this summary.'
	@echo 'update - Pull all git repos recursively.'
	@echo 'build - Build the Jekyll files.'
	@echo 'venv - Update the required Python venv.'

update:
	git submodule update --init --recursive
	git submodule foreach --recursive git pull

build: _venv
	. _venv/bin/activate && _src/scripts/generate.py

_venv: _venv/bin/activate _venv/.updated

_venv/bin/activate:
	virtualenv _venv

_venv/.updated: _src/requirements.txt
	. _venv/bin/activate && pip install -r _src/requirements.txt
	touch $@
