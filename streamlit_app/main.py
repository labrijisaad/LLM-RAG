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

from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials


def main():
    # Set up the main configuration for the Streamlit page
    st.set_page_config(page_title="LLM RAG Application", page_icon="🪄")
    st.title(":red[LLM RAG] - Application")

    # Load credentials and configuration settings for the application
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    app_config = load_models_config("config/models_config.yml")
    knowledge_base_dir = "data/processed"

    # Initialize sidebar elements and retrieve selected settings
    (
        selected_embedding_model_name,
        selected_embedding_model_cost,
        selected_llm_name,
        selected_llm_temp,
        selected_llm_tokens_limit,
    ) = configure_sidebar(app_config)

    # Create tabs for the application interface
    setup_kb_tab, view_kb_tab, rag_query_tab = st.tabs(
        ["Setup Knowledge Base", "Explore Knowledge Base", "RAG Query"]
    )

    # Tab for setting up the Knowledge Base
    with setup_kb_tab:
        setup_knowledge_base_tab(
            openai_api_key, app_config, selected_embedding_model_name
        )

    # Tab for displaying and exploring the Knowledge Base
    with view_kb_tab:
        # Create a QueryPipeline instance to interact with the Knowledge Base
        query_pipeline_instance = QueryPipeline(openai_api_key, app_config)
        # Load and process the Knowledge Base documents
        query_pipeline_instance.load_and_merge_databases(knowledge_base_dir)
        # Filter out empty documents
        processed_documents = [
            doc for doc in query_pipeline_instance.embedder.texts if doc.strip()
        ]
        # Display the documents in the Knowledge Base tab
        display_knowledge_base_tab(processed_documents)

    # Tab for performing queries using the RAG model
    with rag_query_tab:
        initialize_rag_query_tab(
            selected_llm_name, selected_llm_temp, selected_llm_tokens_limit
        )


if __name__ == "__main__":
    main()
