.PHONY: help dev build
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



# 安装python 和 搭建虚拟环境
dev:
	@python3 -m venv venv

# 进入虚拟环境
build: dev
	. $(VENV_ACTIVATE) && pip3 install -r requirements.txt && $(PYTHON) -m nuitka --standalone --onefile --output-dir=build --show-progress --show-memory --follow-imports  $(SRC)/main.py -o /usr/local/DPM/dpm && deactivate && rm -rf venv/ build/ && cd / && rm -rf /usr/local/DPM/TEMP/DPM_SRC && exit 0
