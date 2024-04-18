# Variables
IMAGE_NAME := llm_rag_app
CONTAINER_NAME := llm_rag_app_container
SECRETS_VOLUME_PATH := $(CURDIR)/secrets
PROJECT_ID := llm-rag-application
REPO_NAME := llm-rag
REGION := europe-west1
TAG := latest
IMAGE_URI := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME):$(TAG)

# Default target
.DEFAULT_GOAL := help

# Activate the virtual environment and run Jupyter Lab
jupy:
	@echo Starting Jupyter Lab...
	@jupyter lab

# Run the Streamlit app from the local system
stream:
	@echo Launching Streamlit app...
	@streamlit run streamlit_app/main.py

# Run tests with pytest
test:
	@echo Running tests with pytest...
	@pytest tests/

# Build the Docker image from the Dockerfile
docker-build:
	@echo Building Docker image named $(IMAGE_NAME)...
	@docker build -t $(IMAGE_NAME) -f docker/Dockerfile .

# Tag the Docker image for Google Artifact Registry
docker-tag:
	@echo Tagging Docker image $(IMAGE_NAME)...
	@docker tag $(IMAGE_NAME) $(IMAGE_URI)

# Push the Docker image to Google Artifact Registry
docker-push:
	@echo Pushing Docker image to $(IMAGE_URI)...
	@docker push $(IMAGE_URI)

# Pull the Docker image from Google Artifact Registry
docker-pull:
	@echo Pulling Docker image from $(IMAGE_URI)...
	@docker pull $(IMAGE_URI)

# Run the pulled Docker container with the Streamlit app
docker-run-pulled:
	@echo Running Docker container named $(CONTAINER_NAME)...
	@docker run -d --name $(CONTAINER_NAME) -p 8501:8501 -v "$(SECRETS_VOLUME_PATH):/app/secrets" $(IMAGE_URI)

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
	@echo   make docker-tag      - Tag the Docker image for Google Artifact Registry
	@echo   make docker-push     - Push the Docker image to Google Artifact Registry
	@echo   make docker-pull     - Pull the Docker image from Google Artifact Registry
	@echo   make docker-run-pulled - Run the Streamlit app in a Docker container (pulled image)
	@echo   make docker-run      - Run the Streamlit app in a Docker container
	@echo   make docker-kill     - Stop and remove the Docker container
	@echo Author: $(AUTHOR)