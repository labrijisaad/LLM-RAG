import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from streamlit_app.app_utils.knowledge_base import setup_database, view_database
from streamlit_app.app_utils.sidebar import setup_sidebar
from streamlit_app.app_utils.rag import setup_rag

from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials


def main():
    st.set_page_config(page_title="LLM RAG Application", page_icon="🪄")
    st.title(":red[LLM RAG] - Application")

    # Global parameters and config/secrets loading
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")

    (
        selected_embedding_model,
        selected_embedding_model_price,
        selected_llm_model,
        selected_llm_temperature,
        selected_max_llm_tokens_completion,
    ) = setup_sidebar(models_config)

    tab1, tab2, tab3 = st.tabs(
        ["Knowledge Base Setup", "View Knowledge Base", "RAG Query"]
    )

    with tab1:
        setup_database(openai_api_key, models_config, selected_embedding_model)

    with tab2:
        st.header("View Content of the Knowledge Base")

        # Create an instance of the QueryPipeline and load the knowledge base
        query_pipeline = QueryPipeline(openai_api_key, models_config)
        # query_pipeline.set_model(selected_embedding_model)
        directory_path = "data/processed"
        query_pipeline.load_and_merge_databases(directory_path)

        # Load texts and remove any empty strings
        all_texts = [text for text in query_pipeline.embedder.texts if text.strip()]

        view_database(all_texts)

    with tab3:
        st.header("Perform RAG Query")
        setup_rag()


if __name__ == "__main__":
    main()
