import streamlit as st
import time
import string

from .others import read_file_content, search_documents


def setup_knowledge_base_tab(
    query_pipeline,
    selected_embedding_model,
    output_directory,
    selected_embedding_model_cost,
):
    st.header("📁 Setup :green[Knowledge Base]")
    uploaded_files = st.file_uploader(
        "Upload **:blue[Markdown Files]**",
        type=["md"],
        accept_multiple_files=True,
        help="Upload markdown files for processing.",  # TODO
    )

    if uploaded_files:
        uploaded_file_names = ", ".join(["'" + f.name + "'" for f in uploaded_files])
        st.info(f"**Uploaded Files:** **`{uploaded_file_names}`**", icon="🤖")

        markdown_content = ""
        for uploaded_file in uploaded_files:
            with st.expander(f":red[View Content of **`{uploaded_file.name}`**]"):
                file_content = read_file_content(uploaded_file)
                markdown_content += file_content + "\n"
                st.text(file_content)

        if st.button("Add documents to **:green[Knowledge Base]**", key="create_db"):
            with st.spinner("Creating database from files..."):

                print(markdown_content)

                start_time = time.time()
                total_cost, total_documents_processed = (
                    query_pipeline.setup_semantic_database(
                        markdown_path="",
                        embedding_model=selected_embedding_model,
                        save_index=True,
                        directory_path=output_directory,
                        markdown_content=markdown_content,
                    )
                )

                end_time = time.time()
                elapsed_time = end_time - start_time

                # Formatting Cost and Price
                elapsed_time_formatted = f"{elapsed_time:.2f} seconds"
                formatted_cost = f"$ {total_cost:.8f}"

                st.success(
                    f"File(s) are added successfully to the knowledge base! Total cost: **:red[{formatted_cost}]**",
                    icon="✅",
                )

                # Summary metrics
                detailed_summary_table = f"""
                | Metric | Details | Value |
                | :--- | :--- | :---: |
                | ⏱ **Time Taken** | Total time to process and add files to the knowledge base. | **:green[{elapsed_time_formatted}]** |
                | 💰 **Total Estimated Cost** | Cost estimated based on the processing required for the uploaded documents. | **:green[{formatted_cost}]** |
                | 🤖 **Embedding Model Used** | AI model used to create embeddings for the knowledge base. | **:green[{selected_embedding_model}]** |
                | 📄 **Total Documents Processed** | Number of documents added to the knowledge base. | **:red[{total_documents_processed}]** |
                | 💵 **Model Cost Per Token** | The cost per Token of processing with the selected model. | $ {selected_embedding_model_cost:.8f} |
                """

                with st.expander("Detailed Summary", expanded=True):
                    st.markdown(detailed_summary_table)

    else:
        st.info(
            "🤖 Upload **:blue[Markdown Files]** to proceed with **:green[Knowledge Base]** Setup."
        )


def display_knowledge_base_tab(
    all_texts,
    query_pipeline,
    selected_embedding_model,
    knowledge_base_dir
):

    st.header("🔍Explore the :green[Knowledge Base] Content")
    if len(all_texts) == 0:
        st.warning(
            "⚠️ Currently, no databases are loaded. Please navigate to the :red[Setup Knowledge Base] tab to create your knowledge base."
        )
    else:
        # Display basic info about the Knowledge Base
        st.markdown(f"> Total Documents in Knowledge Base `{len(all_texts)}`")

        search_query = st.text_input(  # TODO
            "Enter a search keyword  ",
            "",
            placeholder="Type here...",
            help="Search the knowledge base **:green[by keyword]**. The search results are **limited** to the **:red[top 10 documents]**. #TODO",
        )

        col1, col2, _ = st.columns([6.5, 2, 0.01], gap="large")
        with col1:
            max_documents = st.slider(
                ":red[Maximum Documents to Display]", 1, len(all_texts), 2
            )
        with col2:
            use_semantic_search = st.checkbox(":red[Activate Similarity Search]")

        search = st.button("**:red[Search]**")

        if search:
            if not search_query.strip() or all(
                char in string.punctuation for char in search_query.strip()
            ):
                st.error(
                    "❌ Please enter a valid word. The input should not be only **spaces**, **punctuation**, or **empty**."
                )

            else:
                if use_semantic_search:
                    st.info(
                        "📌 The :red[Similarity Search] feature may sometimes return **less relevant documents**, depending on the **Content** and the **Size** of the :green[knowledge base]."
                    )
                # Filter texts and sort by the number of occurrences of the search query
                with st.spinner("Searching Relevant Documents... 🤔"):
                    filtered_texts = search_documents(
                        max_documents,
                        search_query,
                        all_texts,
                        use_semantic_search,
                        query_pipeline,
                        selected_embedding_model,
                    )
                # Check if any texts match the query
                if not filtered_texts:
                    st.warning(
                        "☹️ No matches found. Please try a different keyword. Or Activate the :red[Similarity Search]"
                    )
                    st.info(
                        "❓ The :red[Similarity Search] feature allows you to **locate** the documents most closely related to your query within the :green[knowledge base]"
                    )
                else:
                    for index, (text, count) in enumerate(filtered_texts, start=1):
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric(label="Occurrences", value=count)
                        with col2:
                            with st.expander(
                                f":green[Document **{index}**]", expanded=False
                            ):
                                st.info(text)
        else:
            filtered_texts = []
            st.info(
                "🤖 Enter a keyword to search the knowledge base, and click on the :red[Search] button!"
            )
