import base64
from io import BytesIO
import os
import glob
import time


def stream_response(response):
    """Stream the response word by word to simulate typing."""
    for word in response.split():
        yield word + " "
        time.sleep(0.02)


def image_to_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    return img_base64


def read_file_content(uploaded_file):
    """
    Function to read and decode the uploaded file.
    """
    return uploaded_file.getvalue().decode("utf-8")


def get_embedding_models(models_config):
    """
    Extract embedding model names and their pricing from the loaded models configuration.
    """
    embedding_models = [
        model
        for group in models_config["models"]
        if group["name"] == "Embedding models"
        for model in group["variants"]
    ]
    model_info = [
        (model["model"], model["usage_price_per_token"]) for model in embedding_models
    ]
    return model_info


def get_llm_models(models_config):
    """
    Extract LLM model names and their input/output pricing from models configuration file.
    """
    llm_models = [
        (
            model["model"],
            model["input_price_per_token"],
            model["output_price_per_token"],
        )
        for group in models_config["models"]
        if "GPT" in group["name"]
        for model in group["variants"]
    ]
    return llm_models


def delete_files(directory):
    # Gather all .json and .bin files
    files_to_delete = glob.glob(os.path.join(directory, "*.json")) + glob.glob(
        os.path.join(directory, "*.bin")
    )

    # Delete the files
    for file_path in files_to_delete:
        os.remove(file_path)


def search_documents(
    num_results,
    search_query,
    all_texts,
    is_semantic,
    query_pipeline,
    selected_embedding_model,
):
    if search_query:
        if not is_semantic:
            # Filter texts and sort by the number of occurrences of the search query
            similar_docs = sorted(
                [
                    (text, text.lower().count(search_query.lower()))
                    for text in all_texts
                    if search_query.lower() in text.lower()
                ],
                key=lambda x: x[1],
                reverse=True,
            )[:num_results]
        else:
            # Use semantic search with the specified embedding model
            query_pipeline.set_model(selected_embedding_model)
            docs = query_pipeline.find_similar_documents(
                query_text=search_query, num_results=num_results
            )
            # None here, because we don't have occurrence count in similarity search
            similar_docs = [(doc, None) for doc in docs]
        return similar_docs
    else:
        return []
