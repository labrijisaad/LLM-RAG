import streamlit as st
from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials


def read_file_content(uploaded_file):
    """Function to read and decode the uploaded file."""
    return uploaded_file.getvalue().decode("utf-8")


def get_embedding_models(models_config):
    """
    Extract embedding model names and their pricing from the loaded models configuration.
    """
    embedding_models = [model for group in models_config['models'] if group['name'] == 'Embedding models' for model in group['variants']]
    model_info = [(model['model'], model['usage_price_per_token']) for model in embedding_models]
    return model_info

def get_llm_models(models_config):
    """
    Extract LLM model names and their input/output pricing from the loaded models configuration.
    """
    llm_models = [
        (model['model'], model['input_price_per_token'], model['output_price_per_token'])
        for group in models_config['models'] 
        if 'GPT' in group['name']  # Assumes that LLMs have 'GPT' in their group name
        for model in group['variants']
    ]
    return llm_models



def main():
    
    st.title("LLM RAG Application")

    # Global parameters and config/secrets loading
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")

    # Sidebar configuration - Embedding Models Settings
    st.sidebar.markdown("## ✔️ OpenAI *Embedding Model* Settings") 
    embedding_model_info = get_embedding_models(models_config)
    model_names = [model[0] for model in embedding_model_info]
    model_prices = {model[0]: model[1] for model in embedding_model_info}
    selected_model = st.sidebar.selectbox("Choose the embedding model", model_names)
    selected_model_price = model_prices[selected_model]
    st.sidebar.markdown(f"Selected Model: **`{selected_model}`**")
    st.sidebar.markdown(f"Price per **1M token**: **`{selected_model_price*1000000:.2f} $`**")
    st.sidebar.markdown(f"---")

    # Sidebar configuration - LLMs Settings
    st.sidebar.markdown("## ⚙️ OpenAI *LLMs* Settings") 
    llm_model_info = get_llm_models(models_config)
    llm_model_names = [model[0] for model in llm_model_info]
    llm_input_prices = {model[0]: model[1] for model in llm_model_info}
    llm_output_prices = {model[0]: model[2] for model in llm_model_info}
    selected_llm_model = st.sidebar.selectbox("Choose the LLM model", llm_model_names)
    st.sidebar.markdown(f"Selected Model: **`{selected_llm_model}`**")
    st.sidebar.markdown(f"Input price per **1K tokens**: **`{llm_input_prices[selected_llm_model]*1000:.4f} $`**")
    st.sidebar.markdown(f"Output price per **1K tokens**: **`{llm_output_prices[selected_llm_model]*1000:.4f} $`**")
    st.sidebar.markdown("## 🔥 Model Temperature")
    temperature = st.sidebar.slider("Select the LLM temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    st.sidebar.markdown(f"Selected Temperature: **`{temperature}`**")
    st.sidebar.markdown("## ⚡ Max Completion Tokens")
    max_tokens = st.sidebar.slider("Select the LLM Max Completion Tokens", min_value=50, value=500, max_value=1500)
    st.sidebar.markdown(f"Selected Max Completion Tokens: **`{max_tokens}`**")
    st.sidebar.markdown(f"---")


    # Quick Links
    st.sidebar.markdown("## 🌐 Connect with Me")
    st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/labrijisaad/) [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/labrijisaad)")
    st.sidebar.markdown("## 🔗 Quick Links")
    st.sidebar.markdown("[View on GitHub](https://github.com/labrijisaad/LLM-RAG)", unsafe_allow_html=True)









    tab1, tab2 = st.tabs(["Database Setup", "RAG Query"])

    with tab1:
        st.header("Setup Database")
        uploaded_files = st.file_uploader("Upload markdown files:", type=['md'], accept_multiple_files=True, help="Upload markdown files for processing.")

        if uploaded_files:
            uploaded_file_names = ", ".join(["'"+f.name+"'" for f in uploaded_files])
            st.success(f"**Uploaded Files:** **`{uploaded_file_names}`**")
            
            markdown_content = ""
            for uploaded_file in uploaded_files:
                with st.expander(f"View Content of **`{uploaded_file.name}`**"):
                    file_content = read_file_content(uploaded_file)
                    markdown_content += file_content + "\n"  
                    st.markdown("### File Content Preview 👀")
                    st.code(file_content, language='markdown')

            query_pipeline = QueryPipeline(openai_api_key, models_config)
            # Directory to save index and texts
            output_directory = "data/processed"
            if st.button("Create Database", key="create_db"):
                with st.spinner("Creating database from files..."):
                      
                    total_cost = query_pipeline.setup_semantic_database(
                        markdown_path="",  
                        embedding_model=selected_model,
                        save_index=True,
                        directory_path=output_directory,
                        markdown_content=markdown_content
                    )
                    st.success(f"Database created successfully! Total cost: ${total_cost}")
            
        else:
            st.info("Upload markdown files to proceed with database setup.")

    with tab2:
        st.header("Perform RAG Query")
        pass

if __name__ == "__main__":
    main()