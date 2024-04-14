import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials
from utils import (
    get_embedding_models,
    get_llm_models,
    read_file_content,
    image_to_base64,
)
from PIL import Image


def main():
    st.set_page_config(page_title="LLM RAG Application", page_icon="🪄")
    st.title(":red[LLM RAG] - Application")

    # Global parameters and config/secrets loading
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")
    logo = Image.open("./streamlit_app/git.png")
    st.sidebar.markdown(
        f'<div style="text-align: center;"><a href="https://github.com/labrijisaad"><img src="data:image/png;base64,{image_to_base64(logo)}" alt="Direct Assurance Logo" width="100"></a></div>',
        unsafe_allow_html=True,
    )

    # Sidebar configuration - Embedding Models Settings
    st.sidebar.title("🔢 OpenAI *Embedding Model* Settings")
    embedding_model_info = get_embedding_models(models_config)
    model_names = [model[0] for model in embedding_model_info]
    model_prices = {model[0]: model[1] for model in embedding_model_info}
    selected_embedding_model = st.sidebar.selectbox(
        "Choose the embedding model",
        model_names,
        help="Sélectionnez parmi les modèles d'OpenAI disponibles. Le choix du modèle affecte la qualité des résultats, le temps d'inférence et le coût associé à chaque requête.",
    )
    selected_embedding_model_price = model_prices[selected_embedding_model]
    st.sidebar.markdown(f"Selected Model: **`{selected_embedding_model}`**")
    st.sidebar.markdown(
        f"Price per **1M token**: **`{selected_embedding_model_price*1000000:.2f} $`**"
    )

    # Sidebar configuration - LLMs Settings
    st.sidebar.title("⚙️ OpenAI *LLMs* Settings")
    llm_model_info = get_llm_models(models_config)
    llm_model_names = [model[0] for model in llm_model_info]
    llm_input_prices = {model[0]: model[1] for model in llm_model_info}
    llm_output_prices = {model[0]: model[2] for model in llm_model_info}
    selected_llm_model = st.sidebar.selectbox(
        "Choose the LLM model",
        llm_model_names,
        help="Sélectionnez parmi les modèles d'OpenAI disponibles. Le choix du modèle affecte la qualité des résultats, le temps d'inférence et le coût associé à chaque requête.",
    )
    st.sidebar.markdown(f"Selected Model: **`{selected_llm_model}`**")
    st.sidebar.markdown(
        f"Input price per **1K tokens**: **`{llm_input_prices[selected_llm_model]*1000:.4f} $`**"
    )
    st.sidebar.markdown(
        f"Output price per **1K tokens**: **`{llm_output_prices[selected_llm_model]*1000:.4f} $`**"
    )
    # Sidebar configuration - Temperature Setting
    st.sidebar.title("🔥 Model Temperature")
    temperature = st.sidebar.slider(
        "Select the LLM temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01,
        help="La température contrôle la créativité du modèle. Une valeur plus élevée génère des réponses plus variées et imprévisibles, tandis qu'une valeur plus basse produit des réponses plus déterministes.",
    )
    st.sidebar.markdown(f"Selected Temperature: **`{temperature}`**")
    # Sidebar configuration - Max Completion Tokens Setting
    st.sidebar.title("⚡ Max Completion Tokens")
    max_tokens = st.sidebar.slider(
        "Select the LLM Max Completion Tokens",
        min_value=50,
        value=500,
        max_value=1500,
        help="La température contrôle la créativité du modèle. Une valeur plus élevée génère des réponses plus variées et imprévisibles, tandis qu'une valeur plus basse produit des réponses plus déterministes.",
    )
    st.sidebar.markdown(f"Selected Max Completion Tokens: **`{max_tokens}`**")

    # Sidebar configuration - Quick Links
    st.sidebar.title("🌐 Connect with Me")
    st.sidebar.markdown(
        """
        <div style="text-align: center;">

        [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/labrijisaad/)
        [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/labrijisaad)
        
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(
        ["Knowledge Base Setup", "RAG Query", "View Knowledge Base"]
    )

    with tab1:
        st.header("Setup Database")
        uploaded_files = st.file_uploader(
            "Upload markdown files:",
            type=["md"],
            accept_multiple_files=True,
            help="Upload markdown files for processing.",
        )

        if uploaded_files:
            uploaded_file_names = ", ".join(
                ["'" + f.name + "'" for f in uploaded_files]
            )
            st.success(f"**Uploaded Files:** **`{uploaded_file_names}`**")

            markdown_content = ""
            for uploaded_file in uploaded_files:
                with st.expander(f"View Content of **`{uploaded_file.name}`**"):
                    file_content = read_file_content(uploaded_file)
                    markdown_content += file_content + "\n"
                    st.markdown("### File Content Preview 👀")
                    st.code(file_content, language="markdown")

            query_pipeline = QueryPipeline(openai_api_key, models_config)
            # Directory to save index and texts
            output_directory = "data/processed"
            if st.button("Create Database", key="create_db"):
                with st.spinner("Creating database from files..."):

                    total_cost = query_pipeline.setup_semantic_database(
                        markdown_path="",
                        embedding_model=selected_embedding_model,
                        save_index=True,
                        directory_path=output_directory,
                        markdown_content=markdown_content,
                    )
                    st.success(
                        f"Database created successfully! Total cost: ${total_cost}"
                    )

        else:
            st.info("Upload markdown files to proceed with database setup.")

    with tab2:
        st.header("Perform RAG Query")
        pass

    with tab3:
        st.header("View Content of the Knowledge Base")

        # Create an instance of the QueryPipeline and load the knowledge base
        query_pipeline = QueryPipeline(openai_api_key, models_config)
        query_pipeline.set_model(selected_embedding_model)
        directory_path = "data/processed"
        query_pipeline.load_and_merge_databases(directory_path)

        # Load texts and remove any empty strings
        all_texts = [text for text in query_pipeline.embedder.texts if text.strip()]

        if len(all_texts) == 0:
            st.warning(
                "No databases were loaded. Please go to the 'Setup Database' tab to create your knowledge base."
            )
        else:
            # Display basic info about the Knowledge Base
            st.markdown(f"- :red[Total Documents] in Knowledge Base `{len(all_texts)}`")

            # Search box for filtering texts
            search_query = st.text_input("Search by keyword", "")
            if search_query:
                # Filter texts and sort by the number of occurrences of the search query
                filtered_texts = sorted(
                    [
                        (text, text.lower().count(search_query.lower()))
                        for text in all_texts
                        if search_query.lower() in text.lower()
                    ],
                    key=lambda x: x[1],
                    reverse=True,
                )[:5]

                # Check if any texts match the query
                if not filtered_texts:
                    st.warning("No matches found. Please try a different keyword.")
                else:
                    for index, (text, count) in enumerate(filtered_texts, start=1):
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric(label="Occurrences", value=count)
                        with col2:
                            with st.expander(f"Text {index} Preview", expanded=True):
                                st.text(text[:75] + "...")  # Show preview of the text
                                if st.button("Show More", key=f"more_{index}"):
                                    st.text_area("Full Text", text, height=130)
            else:
                filtered_texts = []
                st.info("Enter a keyword to search the knowledge base.")


if __name__ == "__main__":
    main()
