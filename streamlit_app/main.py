import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from streamlit_app.app_utils.knowledge_base import (
    setup_knowledge_base_tab,
    display_knowledge_base_tab,
)
from streamlit_app.app_utils.sidebar import configure_sidebar
from streamlit_app.app_utils.rag import initialize_rag_query_tab
from streamlit_app.app_utils.about import about_tab

from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials


def main():
    # Set up the main configuration for the Streamlit page
    st.set_page_config(page_title="LLM RAG Application", page_icon="🪄")
    st.title(":red[LLM RAG] - Application")

    # Load credentials and configuration settings for the application
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")
    knowledge_base_dir = "data/processed"

    # Initialize sidebar elements and retrieve selected settings
    (
        selected_embedding_model_name,
        selected_embedding_model_cost,
        selected_llm_name,
        selected_llm_temp,
        selected_llm_tokens_limit,
    ) = configure_sidebar(models_config, knowledge_base_dir)

    # Create a QueryPipeline instance to interact with the Knowledge Base
    query_pipeline = QueryPipeline(openai_api_key, models_config)

    # Load and process the Knowledge Base documents
    query_pipeline.load_and_merge_databases(knowledge_base_dir)

    # Set the model
    query_pipeline.set_model(selected_llm_name)

    # Create tabs for the application interface
    setup_kb_tab, view_kb_tab, rag_query_tab, setup_about_tab = st.tabs(
        ["Setup Knowledge Base", "Explore Knowledge Base", "RAG Query", "About me"]
    )

    # Tab for setting up the Knowledge Base
    with setup_kb_tab:
        setup_knowledge_base_tab(
            query_pipeline,
            selected_embedding_model_name,
            knowledge_base_dir,
            selected_embedding_model_cost,
        )

    # Tab for displaying and exploring the Knowledge Base
    with view_kb_tab:
        # Filter out empty documents
        processed_documents = [
            doc for doc in query_pipeline.embedder.texts if doc.strip()
        ]
        # Display the documents in the Knowledge Base tab
        display_knowledge_base_tab(processed_documents)

    # Tab for performing queries using the RAG model
    with rag_query_tab:
        initialize_rag_query_tab(
            selected_embedding_model_name,
            query_pipeline,
            selected_llm_name,
            selected_llm_temp,
            selected_llm_tokens_limit,
            processed_documents,
        )
    with setup_about_tab:
        about_tab()


if __name__ == "__main__":
    main()
