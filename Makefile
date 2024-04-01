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

# Initialization of project structure and files
init:
	@mkdir "$(DATA_RAW_DIR)" "$(DATA_PROCESSED_DIR)" "$(DATA_EXTERNAL_DIR)" "$(NOTEBOOKS_DIR)" "$(DOCS_DIR)" 2> NUL || echo "Directories already exist."
	@echo. 2> "$(DATA_RAW_DIR)\$(GITKEEP_FILE)" || echo "File $(DATA_RAW_DIR)\$(GITKEEP_FILE) already exists."
	@echo. 2> "$(DATA_PROCESSED_DIR)\$(GITKEEP_FILE)" || echo "File $(DATA_PROCESSED_DIR)\$(GITKEEP_FILE) already exists."
	@echo. 2> "$(DATA_EXTERNAL_DIR)\$(GITKEEP_FILE)" || echo "File $(DATA_EXTERNAL_DIR)\$(GITKEEP_FILE) already exists."
	@echo. 2> "$(NOTEBOOKS_DIR)\$(GITKEEP_FILE)" || echo "File $(NOTEBOOKS_DIR)\$(GITKEEP_FILE) already exists."
	@echo. 2> "$(DOCS_DIR)\$(GITKEEP_FILE)" || echo "File $(DOCS_DIR)\$(GITKEEP_FILE) already exists."
	@echo # Project Title > "$(README_FILE)"
	@echo. >> "$(README_FILE)"
	@echo ## Connect >> "$(README_FILE)"
	@echo - 🔗 Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/labrijisaad/) >> "$(README_FILE)"
	@echo author: labriji saad > "$(CONFIG_FILE)"
	@echo # Add your environment variables here > "$(ENV_FILE)"
	@echo # Add files and directories to ignore in version control > "$(GITIGNORE_FILE)"
	@echo # Add your project dependencies here > "$(REQUIREMENTS_FILE)"
	@echo jupyterlab >> "$(REQUIREMENTS_FILE)"  # Add jupyterlab as a default requirement
	@echo ipywidgets >> "$(REQUIREMENTS_FILE)"  # Add ipywidgets as a default requirement
	@echo ">>>>>> Project structure initialized successfully <<<<<<"

# Setup the virtual environment and install dependencies
setup:
	@python -m venv $(VENV_NAME)
	@$(VENV_ACTIVATE)
	@python.exe -m pip install --upgrade pip
	@pip install -r $(REQUIREMENTS_FILE)
	@echo ">>>>>> Environment is ready <<<<<<"

# Update dependencies in the virtual environment
update:
	@$(VENV_ACTIVATE) && python.exe -m pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)
	@echo ">>>>>> Dependencies updated <<<<<<"

# Activate the virtual environment and run Jupyter Lab
jupy:
	@$(VENV_ACTIVATE) && jupyter lab
	@echo ">>>>>> Jupyter Lab is running <<<<<<"

# Clean up the virtual environment and generated files
clean:
	@$(DELETE_CMD) $(VENV_NAME)
	@echo ">>>>>> Cleaned up environment <<<<<<"

# Display available make targets
help:
	@echo Available targets:
	@echo   make init                                             - Initialize the project's structure and essential files
	@echo   make setup                                            - Create a virtual environment and install dependencies
	@echo   make update                                           - Update dependencies in the virtual environment
	@echo   make clean                                            - Clean up the virtual environment and generated files
	@echo   make jupy                                             - Activate the virtual environment and run Jupyter Lab
	@echo Author: $(AUTHOR)