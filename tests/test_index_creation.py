from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials
import os


def test_index_creation(tmpdir):
    output_directory = tmpdir.strpath
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")

    query_pipeline = QueryPipeline(openai_api_key, models_config)

    total_cost, total_documents_processed = query_pipeline.setup_semantic_database(
        markdown_path="data/raw/mock_markdown.md",
        embedding_model="text-embedding-3-small",
        save_index=True,
        directory_path=output_directory,
    )

    # Check if the total cost is a float number
    assert isinstance(total_cost, float)

    # Check if the index file (.bin) and texts file (.json) are created in the directory
    files = os.listdir(output_directory)
    print(files)
    assert any(os.path.splitext(f)[1] == ".bin" for f in files)
    assert any(os.path.splitext(f)[1] == ".json" for f in files)
