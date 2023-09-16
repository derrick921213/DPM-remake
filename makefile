.PHONY: help dev upgrade debug
VENV_NAME?=venv
VENV_ACTIVATE=$(shell pwd)/$(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
SRC=src
VERSION ?= V0
IVERSION ?= $(shell sudo python $(SRC)/main.py version)
.DEFAULT: help
help:
	@echo "make dev"
	@echo "       prepare development environment, use only once"
	@echo "make clean"
	@echo "       clean python cache files"
	@echo "make build"
	@echo "       build DPM executable"
	@echo "make venv"
	@echo "       Shell in to venv"
dev:
	@python3 -m venv venv
upgrade: dev
	. $(VENV_ACTIVATE) && \
	pip3 install -r requirements.txt && \
	$(PYTHON) -m nuitka --standalone --onefile --output-dir=build --show-progress  --disable-ccache --follow-imports  $(SRC)/main.py -o dpm.$(VERSION) && \
	deactivate && \
	mv build/dpm.$(VERSION) ../../
install: dev
	. $(VENV_ACTIVATE) && \
	pip3 install -r requirements.txt && \
	version = $(shell sudo $(PYTHON) $(SRC)/main.py version)
	$(PYTHON) -m nuitka --standalone --onefile --output-dir=build --show-progress  --disable-ccache --follow-imports  $(SRC)/main.py -o dpm.$(IVERSION) && \
	deactivate && \
	mkdir -p /usr/local/DPM/TEMP && \
	mv build/dpm.$(IVERSION) /usr/local/DPM/ && \
	cd / && \
	rm -rf $(shell pwd) && \
	ln -s /usr/local/DPM/dpm.$(IVERSION) /usr/local/bin/dpm