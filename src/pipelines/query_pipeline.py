
from ..models.inference import ModelInferenceManager
from ..models.vectorization import SemanticVectorizer

class QueryPipeline:
    def __init__(self, openai_api_key, models_config):
        self.embedder = SemanticVectorizer(openai_api_key, models_config)
        self.model_inference_manager = ModelInferenceManager(
            openai_api_key, models_config
        )

    def setup_semantic_database(self, markdown_path, embedding_model):
        self.embedder.set_model(embedding_model)
        self.embedder.read_and_process_markdown(markdown_path)
        total_cost = self.embedder.generate_embeddings()
        self.embedder.create_faiss_index()
        return total_cost

    def find_similar_documents(self, query_text, num_results):
        similar_docs = self.embedder.search_similar_sections(query_text, num_results)
        return similar_docs

    def determine_expertise_and_prepare_prompt(
        self,
        user_query,
        similar_docs,
        inference_model,
        max_completion_tokens,
        temperature,
    ):
        self.model_inference_manager.set_model(inference_model)
        identified_expertise_area, expertise_area_usage = (
            self.model_inference_manager.determine_expertise_area(
                user_query, max_completion_tokens, temperature
            )
        )
        # Calculate the cost for determining expertise area
        expertise_area_cost = 0  # Default to 0
        if expertise_area_usage:
            expertise_area_cost = self.model_inference_manager.calculate_cost(
                expertise_area_usage
            )
        context_enhanced_prompt = self.model_inference_manager.prepare_prompt_for_llm(
            identified_expertise_area, user_query, similar_docs
        )
        return context_enhanced_prompt, expertise_area_cost

    def query_model_for_response(
        self, context_enhanced_prompt, max_completion_tokens, temperature
    ):
        contextual_response, response_usage = self.model_inference_manager.query_openai(
            context_enhanced_prompt, max_completion_tokens, temperature
        )
        # Calculate the cost for querying the model
        response_cost = 0  # Default to 0
        if response_usage:
            response_cost = self.model_inference_manager.calculate_cost(response_usage)

        return contextual_response, response_cost