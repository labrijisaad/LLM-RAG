from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials

def main():
    # Load OpenAI API Key and Model Configurations
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")

    # Initialize the QueryPipeline
    query_pipeline = QueryPipeline(openai_api_key, models_config)

    # Set the model
    query_pipeline.set_model("text-embedding-3-small")

    # Load and merge the semantic database FAISS indexes and the texts
    directory_path = "data/processed"
    # Assuming `load_and_merge_databases` is properly implemented to handle
    # the loading and merging process.
    query_pipeline.load_and_merge_databases(directory_path)

    # Example query
    user_query = input("Enter your query: ")

    # Proceed with the rest of the querying process
    similar_docs = query_pipeline.find_similar_documents(query_text=user_query, num_results=2)

    context_enhanced_prompt, expertise_area_cost = (
        query_pipeline.determine_expertise_and_prepare_prompt(
            user_query=user_query,
            similar_docs=similar_docs,
            inference_model="gpt-3.5-turbo-0125",
            max_completion_tokens=150,
            temperature=0.2,
        )
    )
    print(f"Cost for determining expertise area: {expertise_area_cost}")

    contextual_response, response_cost = query_pipeline.query_model_for_response(
        context_enhanced_prompt=context_enhanced_prompt,
        max_completion_tokens=1500,
        temperature=0.7,
    )
    print(f"Cost for querying the model for a response: {response_cost}")

    # Output the response
    print("--------\nContextual Prompt:\n--------")
    print(context_enhanced_prompt)
    print("--------\nResponse:\n--------")
    print(contextual_response)

if __name__ == "__main__":
    main()