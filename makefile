.PHONY: help dev upgrade
VENV_NAME?=venv
VENV_ACTIVATE=$(shell pwd)/$(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
SRC=src
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
	@. $(VENV_ACTIVATE) && \
	pip3 install -r requirements.txt && \
	$(PYTHON) -m nuitka --standalone --onefile --output-dir=build --show-progress  --follow-imports  $(SRC)/main.py -o dpm && \
	deactivate && \
	mv build/dpm ../../ && \
	rm -rf venv/ build/ && \
	cd / && \
	rm -rf /usr/local/DPM/TEMP/DPM_SRC /usr/local/bin/dpm && \
	ln -s /usr/local/DPM/dpm /usr/local/bin && \
	echo "請按下enter結束"
install: dev
	@. $(VENV_ACTIVATE) && \
	pip3 install -r requirements.txt && \
	$(PYTHON) -m nuitka --standalone --onefile --output-dir=build --show-progress  --follow-imports  $(SRC)/main.py -o dpm && \
	deactivate && \
	mv build/dpm /usr/local/DPM && \
	cd / && \
	rm -rf $(shell pwd) && \
	ln -s /usr/local/DPM/dpm /usr/local/bin