import streamlit as st

from PIL import Image
from app_utils.others import get_embedding_models, get_llm_models, image_to_base64


def configure_sidebar(models_config):
    logo = Image.open("./streamlit_app/app_logo.png")
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
        help="Choose from available OpenAI embedding models. Model choice affects result quality, inference time, and cost per query.",
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
        help="Choose from available OpenAI LLMs. Model choice affects result quality, inference time, and cost per query.",
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
    selected_llm_temperature = st.sidebar.slider(
        "Select the LLM temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01,
        help="Control the model's creativity. Higher values yield more varied, unpredictable responses, while lower values are more deterministic.",
    )
    st.sidebar.markdown(f"Selected Temperature: **`{selected_llm_temperature}`**")
    # Sidebar configuration - Max Completion Tokens Setting
    st.sidebar.title("⚡ Max Completion Tokens")
    selected_llm_max_tokens_completion = st.sidebar.slider(
        "Select the LLM Max Completion Tokens",
        min_value=50,
        value=500,
        max_value=3500,
        help="Set the max number of tokens for LLM to generate. Affects response length and processing time.",
    )
    st.sidebar.markdown(
        f"Selected Max Completion Tokens: **`{selected_llm_max_tokens_completion}`**"
    )

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
    return (
        selected_embedding_model,
        selected_embedding_model_price,
        selected_llm_model,
        selected_llm_temperature,
        selected_llm_max_tokens_completion,
    )
