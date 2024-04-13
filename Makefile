# Variables
VENV_NAME := venv
DATA_RAW_DIR := data/raw
DATA_PROCESSED_DIR := data/processed
DATA_EXTERNAL_DIR := data/external
NOTEBOOKS_DIR := notebooks
DOCS_DIR := docs
README_FILE := README.md
CONFIG_FILE := config.yaml
ENV_FILE := .env
GITIGNORE_FILE := .gitignore
REQUIREMENTS_FILE := requirements.txt
GITKEEP_FILE := .gitkeep
AUTHOR := labriji saad

# Default target
.DEFAULT_GOAL := help

# Detect OS and set commands accordingly
OSFLAG :=
ifeq ($(OS),Windows_NT)
    OSFLAG += -D WIN32
    ifeq ($(PROCESSOR_ARCHITEW6432),AMD64)
        OSFLAG += -D AMD64
    else
        ifeq ($(PROCESSOR_ARCHITECTURE),AMD64)
            OSFLAG += -D AMD64
        endif
        ifeq ($(PROCESSOR_ARCHITECTURE),x86)
            OSFLAG += -D IA32
        endif
    endif
    DELETE_CMD := del /F /Q
    VENV_ACTIVATE := .\$(VENV_NAME)\Scripts\activate
    MKDIR_CMD := mkdir
    POWERSHELL_CMD := powershell
else
    DELETE_CMD := rm -rf
    VENV_ACTIVATE := source $(VENV_NAME)/bin/activate
    MKDIR_CMD := mkdir -p
    POWERSHELL_CMD := pwsh
endif

# Activate the virtual environment and run Jupyter Lab
jupy:
	@$(VENV_ACTIVATE) && jupyter lab
	@echo ">>>>>> Jupyter Lab is running <<<<<<"

app:
	@$(VENV_ACTIVATE)
	@python app.py

app2:
	@$(VENV_ACTIVATE)
	@python app2.py

stream:
	@$(VENV_ACTIVATE)
	@streamlit run .\streamlit_app.py

test:
	@$(VENV_ACTIVATE)
	@pytest tests/

# Display available make targets
help:
	@echo Available targets:
	@echo   make jupy                                             - Activate the virtual environment and run Jupyter Lab
	@echo   make test                                             - Tests the code using pytest
	@echo   make app                                              - Runs the App
	@echo   make app2                                             - Runs the App2
	@echo   make stream                                           - Runs the streamlit app
	@echo Author: $(AUTHOR)