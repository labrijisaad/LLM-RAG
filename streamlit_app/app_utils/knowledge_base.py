import streamlit as st
from src.pipelines.query_pipeline import QueryPipeline
from .others import read_file_content


def setup_knowledge_base_tab(openai_api_key, models_config, selected_embedding_model):
    st.header("📁 Setup :green[Knowledge Base]")
    uploaded_files = st.file_uploader(
        "Upload :red[Markdown] Files:",
        type=["md"],
        accept_multiple_files=True,
        help="Upload markdown files for processing.",
    )

    if uploaded_files:
        uploaded_file_names = ", ".join(["'" + f.name + "'" for f in uploaded_files])
        st.success(f"**Uploaded Files:** **`{uploaded_file_names}`**")

        markdown_content = ""
        for uploaded_file in uploaded_files:
            with st.expander(f"👀 View Content of **`{uploaded_file.name}`** file"):
                file_content = read_file_content(uploaded_file)
                markdown_content += file_content + "\n"
                st.text(file_content)

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
                st.success(f"Database created successfully! Total cost: ${total_cost}")

    else:
        st.info("Upload markdown files to proceed with database setup.")


def display_knowledge_base_tab(all_texts):
    st.header("🔍Explore the :green[Knowledge Base] Content")
    if len(all_texts) == 0:
        st.warning(
            "No databases were loaded. Please go to the 'Setup Database' tab to create your knowledge base."
        )
    else:
        # Display basic info about the Knowledge Base
        st.markdown(f"📜 :red[Total Documents] in Knowledge Base `{len(all_texts)}`")

        # Search box for filtering texts
        search_query = st.text_input(
            "Enter a search keyword  ( :red[Note: A maximum of **10** documents will be displayed] )",
            "",
            placeholder="Type here...",
            help="Search the knowledge base by keyword. The search results are limited to the top 10 documents.",
        )
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
            )[:10]

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
