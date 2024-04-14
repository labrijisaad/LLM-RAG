import base64
from io import BytesIO


def image_to_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    return img_base64


def read_file_content(uploaded_file):
    """Function to read and decode the uploaded file."""
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
    Extract LLM model names and their input/output pricing from the loaded models configuration.
    """
    llm_models = [
        (
            model["model"],
            model["input_price_per_token"],
            model["output_price_per_token"],
        )
        for group in models_config["models"]
        if "GPT" in group["name"]  # Assumes that LLMs have 'GPT' in their group name
        for model in group["variants"]
    ]
    return llm_models
