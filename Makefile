# Variables
IMAGE_NAME := llm_rag_app
CONTAINER_NAME := llm_rag_app_container
SECRETS_VOLUME_PATH := $(CURDIR)/secrets

# Default target
.DEFAULT_GOAL := help

# Activate the virtual environment and run Jupyter Lab
jupy:
	@echo Starting Jupyter Lab...
	@$(VENV_ACTIVATE) && jupyter lab

# Run the Streamlit app from the local system
stream:
	@echo Launching Streamlit app...
	@$(VENV_ACTIVATE) && streamlit run streamlit_app/main.py

# Run tests with pytest
test:
	@echo Running tests with pytest...
	@$(VENV_ACTIVATE) && pytest tests/

# Build the Docker image from the Dockerfile
docker-build:
	@echo Building Docker image named $(IMAGE_NAME)...
	@docker build -t $(IMAGE_NAME) -f docker/Dockerfile .

# Run the Docker container with the Streamlit app
docker-run:
	@echo Running Docker container named $(CONTAINER_NAME)...
	@docker run -d --name $(CONTAINER_NAME) -p 8501:8501 -v "$(SECRETS_VOLUME_PATH):/app/secrets" $(IMAGE_NAME)

# Stop and remove the Docker container
docker-kill:
	@echo Stopping and removing Docker container named $(CONTAINER_NAME)...
	@docker stop $(CONTAINER_NAME)
	@docker rm $(CONTAINER_NAME)

# Display available make targets and their descriptions
help:
	@echo Available targets:
	@echo   make jupy            - Activate the virtual environment and run Jupyter Lab
	@echo   make test            - Run the tests for the application with pytest
	@echo   make stream          - Start the Streamlit app from the local system
	@echo   make docker-build    - Build the Docker image for the application
	@echo   make docker-run      - Run the Streamlit app in a Docker container
	@echo   make docker-kill     - Stop and remove the Docker container
	@echo Author: $(AUTHOR)