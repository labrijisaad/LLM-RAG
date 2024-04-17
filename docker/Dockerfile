FROM python:3.8.12-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the necessary directories and files to the container
COPY src/ src/
COPY data/ /app/data/
COPY streamlit_app/ streamlit_app/
COPY config/ config/
COPY docker/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available outside this container
EXPOSE 8501

# Define the volume for secrets
VOLUME /app/secrets

# Run the Streamlit app using the entry point main.py within the streamlit_app directory
CMD ["streamlit", "run", "streamlit_app/main.py"]
