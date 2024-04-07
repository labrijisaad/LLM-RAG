from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials


def main():
    # Load OpenAI API Key and Model Configurations
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")

    # Initialize the QueryPipeline
    query_pipeline = QueryPipeline(openai_api_key, models_config)

    # Set up the semantic database (example path and model)
    total_cost = query_pipeline.setup_semantic_database(
        markdown_path="data/raw/mock_markdown.md",
        embedding_model="text-embedding-3-small",
        save_index=True,
        index_path="data/processed/faiss_index.bin",
    )
    print(f"Total cost for setting up the semantic database: ${total_cost}")

    # Example query
    user_query = input("Enter your query: ")

    # Find similar documents
    similar_docs = query_pipeline.find_similar_documents(
        query_text=user_query, num_results=3
    )

    # Determine expertise area and prepare the prompt
    context_enhanced_prompt, expertise_area_cost = (
        query_pipeline.determine_expertise_and_prepare_prompt(
            user_query=user_query,
            similar_docs=similar_docs,
            inference_model="gpt-3.5-turbo-0125",
            max_completion_tokens=150,
            temperature=0.2,
        )
    )
    print(f"Cost for determining expertise area: ${expertise_area_cost}")

    # Query the model for a response
    contextual_response, response_cost = query_pipeline.query_model_for_response(
        context_enhanced_prompt=context_enhanced_prompt,
        max_completion_tokens=1500,
        temperature=0.7,
    )
    print(f"Cost for querying the model for a response: ${response_cost}")

    # Output the response
    print("--------\nContextual Prompt:\n--------")
    print(context_enhanced_prompt)
    print("--------\nResponse:\n--------")
    print(contextual_response)


if __name__ == "__main__":
    main()
