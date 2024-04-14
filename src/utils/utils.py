import yaml
import re
import os


def load_credentials(credentials_path="secrets/credentials.yml"):
    """
    Load credentials from the environment or a YAML file. ( depends on the environment )
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return {"OPENAI_CREDENTIALS": openai_api_key}

    with open(credentials_path, "r") as credentials_file:
        return yaml.safe_load(credentials_file)


def load_models_config(config_file_path):
    """
    Load models configuration from a YAML file.

    Parameters:
    config_file_path (str): The path to the YAML file containing the models' configurations.

    Returns:
    dict or None: The models configuration dictionary if the file is found and properly formatted, otherwise None.
    """
    with open(config_file_path, "r") as config_file:
        try:
            models_config = yaml.safe_load(config_file)
            return models_config
        except yaml.YAMLError as exc:
            print(f"Error loading models configuration: {exc}")
            return None


def split_markdown_by_headers(markdown_content):
    pattern = re.compile(r'(?m)(^#{1,6}\s.*$)')
    parts = pattern.split(markdown_content)
    sections = []
    current_header = None
    for part in parts:
        if pattern.match(part):
            current_header = part.strip()
        elif part.strip():
            if current_header:
                sections.append(f"{current_header}\n{part.strip()}")
            else:
                sections.append(part.strip())
    return sections