from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials
import json
import os


def test_rag_query():
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")
    directory_path = "data/processed"

    query_pipeline = QueryPipeline(openai_api_key, models_config)
    query_pipeline.set_model("text-embedding-3-small")
    query_pipeline.load_and_merge_databases(directory_path)

    # Load all text documents from JSON files in the directory
    all_original_docs = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), "r") as file:
                docs = json.load(file)
                all_original_docs.extend(docs)

    # Mock a query
    user_query = "test query"
    print(f"Querying with: '{user_query}'")

    # Execute the RAG query process
    similar_docs = query_pipeline.find_similar_documents(
        query_text=user_query, num_results=2
    )

    # Print the similar documents
    print("Similar documents found:")
    for doc in similar_docs:
        print(doc)

    # Assert that similar documents returned is a list
    assert isinstance(similar_docs, list), "The result should be a list."

    # Assert that each similar document is a string and exists in the concatenated list of original documents
    assert all(
        isinstance(doc, str) for doc in similar_docs
    ), "Each item in results should be a string."
    assert all(
        doc in all_original_docs for doc in similar_docs
    ), "Each similar document should be in the list of all original documents."
