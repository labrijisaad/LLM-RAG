import streamlit as st
from .others import stream_response
import time


def initialize_rag_query_tab(
    selected_embedding_model_name,
    query_pipeline,
    selected_llm_name,
    selected_llm_temp,
    selected_llm_tokens_limit,
    processed_documents,
):
    # Display header for RAG queries
    st.header("⚡Execute :green[RAG] Queries")

    # Get the total number of documents in the knowledge base
    total_docs_in_knowledge_base = len(processed_documents)

    # Ensure there are documents in the knowledge base
    if total_docs_in_knowledge_base == 0:
        st.error(
            "The knowledge base is currently empty. Please upload documents to the 'Setup Database' tab."
        )
        return

    # User input for number of results to include in the context
    num_results = st.number_input(
        "Select number of documents to include in the context",
        min_value=1,
        max_value=total_docs_in_knowledge_base,
        value=min(2, total_docs_in_knowledge_base),
        step=1,
        help="Specify how many of the most relevant documents you want to include for generating the response. This helps in refining the context for more accurate answers.",
    )

    # User input for query
    user_query = st.text_input(
        "Type the Question to ask the RAG LLM",
        "",
        placeholder="What would you like to know?",
        help="Enter your question here. The system will retrieve relevant documents from the knowledge base and use them to generate a detailed and contextually accurate response. This allows the RAG model to leverage specific knowledge and provide answers that are not only accurate but also deeply informed by the existing documents.",
    )

    # Execute only if user query is provided
    if user_query:
        start_time = time.time()
        with st.spinner("Finding similar documents..."):
            query_pipeline.set_model(selected_embedding_model_name)
            similar_docs = query_pipeline.find_similar_documents(
                query_text=user_query, num_results=num_results
            )

            if not similar_docs:
                st.error("No similar documents found.")
            else:
                with st.expander(
                    "Used **:green[Relevent Documents]** in Context", expanded=False
                ):
                    for doc in similar_docs:
                        st.info(doc)

        # Prepare context-enhanced prompt
        with st.spinner("Preparing context-enhanced prompt..."):
            context_enhanced_prompt, expertise_area_cost, identified_expertise_area = (
                query_pipeline.determine_expertise_and_prepare_prompt(
                    user_query=user_query,
                    similar_docs=similar_docs,
                    inference_model=selected_llm_name,
                    max_completion_tokens=selected_llm_tokens_limit,
                    temperature=selected_llm_temp,
                )
            )
            with st.expander("RAG Prompt", expanded=True):
                st.info(
                    f"Identified Expertise Area: **:red[{identified_expertise_area}]**"
                )
                st.success(
                    f"Cost for expertise area determination: **:red[$ {expertise_area_cost:.6f}]**"
                )

        with st.expander("Final **:green[RAG] Prompt**", expanded=False):
            st.text(context_enhanced_prompt)

        # Generate response
        with st.spinner("Generating the response... 🤔"):
            contextual_response, response_cost = (
                query_pipeline.query_model_for_response(
                    context_enhanced_prompt=context_enhanced_prompt,
                    max_completion_tokens=selected_llm_tokens_limit,
                    temperature=selected_llm_temp,
                )
            )

        # Display message
        st.chat_message("assistant").write_stream(stream_response(contextual_response))

        # Display summary of costs and steps with enhanced visual and detailed tooltips
        with st.expander("📊 Detailed Summary of Inference", expanded=True):
            # Metrics for display
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Formatting Cost and Price
            elapsed_time_formatted = f"{elapsed_time:.2f} seconds"
            formatted_cost = f"$ {(response_cost + expertise_area_cost):.4f}"

            # Display detailed summary of inference
            detailed_summary_table = f"""
                | Metric | Details | Value |
                | :--- | :--- | :---: |
                | ⏱ **Time Taken** | Total time taken to process the query and generate the response. | **:green[{elapsed_time_formatted}]** |
                | 💵 **Total Estimated Cost** | Cost estimated based on the processing and querying with the RAG model. | **:green[{formatted_cost}]** |
                | 🤖 **LLM Model Used** | AI model used for generating the response. | **:green[{selected_llm_name}]** |
                """

            st.markdown(detailed_summary_table, unsafe_allow_html=True)
