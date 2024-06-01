import numpy as np
import datetime
import os
import faiss
import json

from ..models.inference import ModelInferenceManager
from ..models.vectorization import SemanticVectorizer
from ..utils.utils import split_markdown_by_headers_with_hierarchy


class QueryPipeline:
    def __init__(self, openai_api_key, models_config):
        self.embedder = SemanticVectorizer(openai_api_key, models_config)
        self.model_inference_manager = ModelInferenceManager(
            openai_api_key, models_config
        )

    def set_model(self, model_name):
        self.embedder.set_model(model_name)
        # Assuming you might also need to set the model in ModelInferenceManager if necessary.

    def setup_semantic_database(
        self,
        markdown_path=None,
        embedding_model=None,
        save_index=False,
        directory_path=None,
        markdown_content=None,
    ):
        # Ensure the embedding model is set
        self.embedder.set_model(embedding_model)

        # Check if content is directly provided, otherwise read from the path
        if markdown_content:
            # Directly use provided markdown content
            texts = split_markdown_by_headers_with_hierarchy(markdown_content)
        elif markdown_path:
            # Read and process markdown file if path is provided
            texts = self.embedder.read_and_process_markdown(markdown_path)

        total_cost = 0
        total_documents_processed = 0

        # Iterate over each text chunk and process them individually
        for i, text in enumerate(texts):
            # Set the current text to the embedder
            self.embedder.texts = [text]

            # Reset embeddings for each chunk
            self.embedder.embeddings = []

            # Generate embeddings and calculate the cost for each chunk
            cost = self.embedder.generate_embeddings()

            # Update the total cost
            total_cost += cost

            if save_index and directory_path:
                # Generate unique filenames for saving the index and texts
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                index_filename = f"faiss_db_chunk_{i}_{timestamp}.bin"
                texts_filename = f"faiss_db_chunk_{i}_{timestamp}.json"

                # Generate full file paths
                index_path = os.path.join(directory_path, index_filename)
                texts_path = os.path.join(directory_path, texts_filename)

                # Save the index and texts for each chunk
                self.embedder.save_faiss_index(index_path, texts_path)

            total_documents_processed += 1

        return total_cost, total_documents_processed

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
        return context_enhanced_prompt, expertise_area_cost, identified_expertise_area

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

    def load_faiss_index(self, index_path):
        """Loads the FAISS index from a specified path."""
        try:
            self.embedder.load_faiss_index(index_path)
        except Exception as e:
            print(f"Error loading FAISS index: {e}")

    def load_and_merge_databases(self, directory_path):
        all_texts = []
        all_embeddings = []

        # Iterate over the files in the given directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".bin"):
                # Construct the full paths for the index and texts files
                index_path = os.path.join(directory_path, filename)
                texts_filename = filename.replace(".bin", ".json")
                texts_path = os.path.join(directory_path, texts_filename)

                # Load FAISS index if both the index and texts files exist
                if os.path.exists(index_path) and os.path.exists(texts_path):
                    faiss_index = faiss.read_index(index_path)

                    with open(texts_path, "r", encoding="utf-8") as f:
                        texts = json.load(f)

                    embeddings = np.zeros(
                        (faiss_index.ntotal, faiss_index.d), dtype="float32"
                    )
                    for i in range(faiss_index.ntotal):
                        embeddings[i, :] = faiss_index.reconstruct(i)

                    all_texts.extend(texts)
                    all_embeddings.append(embeddings)
                else:
                    print(
                        f"Warning: Required files for {filename} are missing. Skipping."
                    )

        # Handle the case with zero or one database file
        if len(all_embeddings) == 0:
            print("No databases were loaded. Please check the directory.")
        elif len(all_embeddings) == 1:
            # When there's only one database, directly use it
            self.embedder.faiss_index = faiss.IndexFlatL2(all_embeddings[0].shape[1])
            self.embedder.faiss_index.add(all_embeddings[0])
            self.embedder.texts = all_texts
        else:
            # Combine and rebuild the index for multiple databases
            combined_embeddings = np.vstack(all_embeddings)
            combined_index = faiss.IndexFlatL2(combined_embeddings.shape[1])
            combined_index.add(combined_embeddings)
            self.embedder.faiss_index = combined_index
            self.embedder.texts = all_texts
