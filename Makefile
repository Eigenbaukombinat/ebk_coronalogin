.DEFAULT_GOAL := install
ENV_DIR = venv
CURRENT_DIR := $(shell pwd)
VENV_BIN_DIR = $(CURRENT_DIR)/$(ENV_DIR)/bin/

$(ENV_DIR)/.installed:
	virtualenv --python=python3 venv
	touch $(ENV_DIR)/.installed

$(ENV_DIR)/.pip_installed: $(ENV_DIR)/.installed
	$(VENV_BIN_DIR)/pip install -r requirements.txt
	touch $(ENV_DIR)/.pip_installed

.PHONY: install
install: $(ENV_DIR)/.pip_installed 

.PHONY: clean
clean:
	rm -rf $(ENV_DIR)
