import streamlit as st
from src.pipelines.query_pipeline import QueryPipeline
from src.utils.utils import load_models_config, load_credentials
import base64

def read_file_content(uploaded_file):
    """Function to read and decode the uploaded file."""
    return uploaded_file.getvalue().decode("utf-8")

def main():
    st.title("LLM RAG Application")
    credentials = load_credentials("secrets/credentials.yml")
    openai_api_key = credentials["OPENAI_CREDENTIALS"]
    models_config = load_models_config("config/models_config.yml")
    query_pipeline = QueryPipeline(openai_api_key, models_config)

    tab1, tab2 = st.tabs(["Database Setup", "RAG Query"])

    with tab1:
        st.header("Setup Database")
        uploaded_files = st.file_uploader("Upload markdown files:", type=['md'], accept_multiple_files=True, help="Upload markdown files for processing.")
        
        if uploaded_files:
            uploaded_file_names = ", ".join([f.name for f in uploaded_files])
            st.success(f"Uploaded Files: {uploaded_file_names}")
            
            for uploaded_file in uploaded_files:
                with st.expander(f"View Content of {uploaded_file.name}"):
                    file_content = read_file_content(uploaded_file)
                    st.markdown("## File Content Preview")
                    st.code(file_content, language='markdown')

            if st.button("Create Database", key="create_db"):
                with st.spinner("Creating database from files..."):
                    pass  # Database creation logic
        else:
            st.info("Upload markdown files to proceed with database setup.")

    with tab2:
        st.header("Perform RAG Query")
        user_query = st.text_input("Enter your query:", help="Type your query here and press enter.")
        if user_query:
            if st.button("Query", key="perform_query"):
                with st.spinner("Querying the database..."):
                    pass  # Query execution logic
                # Display query results
                st.subheader("Query Results:")
                st.markdown("Here would be the query results, possibly with highlights and links to source documents.")

if __name__ == "__main__":
    main()