import streamlit as st
from .others import stream_response
import time
import string


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

    if total_docs_in_knowledge_base == 0:
        st.warning(
            "⚠️ No databases loaded. To create your knowledge base, visit the :red[Setup Knowledge Base] tab. the RAG LLM **:red[won't provide contextual answers]** without documents."
        )
        st.info(
            "🤌 You can still ask the :green[LLM RAG], but you won't get any context-based answers. ☹️"
        )

        # User input for query
        user_query = st.text_input(
            "Type the question to ask the :green[RAG LLM]",
            "",
            placeholder="What would you like to know? 😉",
            help="Enter your question here. #TODO",
        )

        message_button = st.button("**:red[Send Message]**")
        if message_button:
            # Execute only if user query is provided
            if not user_query.strip() or all(
                char in string.punctuation for char in user_query.strip()
            ):
                st.error(
                    "❌ Please enter a valid word. The input should not be only **spaces**, **punctuation**, or **empty**."
                )
            else:
                start_time = time.time()
                with st.spinner("Finding similar documents..."):
                    query_pipeline.set_model(selected_embedding_model_name)
                    similar_docs = []

                    if not similar_docs:
                        st.error(
                            "❌ User has chosen not to provide documents from the knowledge base!"
                        )
                    else:
                        with st.expander(
                            "Used **:green[Relevent Documents]** in Context",
                            expanded=False,
                        ):
                            for doc in similar_docs:
                                st.info(doc)

                # Prepare context-enhanced prompt
                with st.spinner("Preparing context-enhanced prompt..."):
                    if len(similar_docs) == 0:
                        similar_docs = [
                            "No documents found related to user query! Use your external knowledge or search the internet if possible"
                        ]
                    (
                        context_enhanced_prompt,
                        expertise_area_cost,
                        identified_expertise_area,
                    ) = query_pipeline.determine_expertise_and_prepare_prompt(
                        user_query=user_query,
                        similar_docs=similar_docs,
                        inference_model=selected_llm_name,
                        max_completion_tokens=selected_llm_tokens_limit,
                        temperature=selected_llm_temp,
                    )
                    with st.expander("Expertise Area Identification", expanded=False):
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
                st.chat_message("assistant").write_stream(
                    stream_response(contextual_response)
                )

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
                        | ⏱ **Time Taken** | Total time taken to process the query and generate the response. | **:red[{elapsed_time_formatted}]** |
                        | 💵 **Cost for Determining Expertise Area** | Cost from the initial prompt to determine the expertise area. | **:red[$ {expertise_area_cost:.6f}]** |
                        | 🤑 **Cost to Query the LLM** | Cost estimated based on the processing and querying with the RAG model. | **:red[{formatted_cost}]** |
                        | 🤖 **LLM Model Used** | AI model used for generating the response. | **:green[{selected_llm_name}]** | 
                        """

                    st.markdown(detailed_summary_table, unsafe_allow_html=True)
    else:
        # Display basic info about the Knowledge Base
        st.markdown(
            f"> Total Documents in Knowledge Base `{total_docs_in_knowledge_base}`"
        )

        # Ensure there are documents in the knowledge base
        if total_docs_in_knowledge_base == 0:
            st.error(
                "The knowledge base is currently empty. Please upload documents to the 'Setup Database' tab."
            )
            return

        # User input for number of results to include in the context
        num_results = st.number_input(
            "Select :green[number of documents] to include in the context",
            max_value=total_docs_in_knowledge_base,
            min_value=0,
            value=2,
            step=1,
            help="Specify how many of the most relevant documents you want to include for generating the response. This helps in refining the context for more accurate answers.",
        )

        # User input for query
        user_query = st.text_input(
            "Type the Question to ask the :green[RAG LLM]",
            "",
            placeholder="What would you like to know? 😉",
            help="Enter your question here. The system will retrieve relevant documents from the knowledge base and use them to generate a detailed and contextually accurate response. This allows the RAG model to leverage specific knowledge and provide answers that are not only accurate but also deeply informed by the existing documents.",
        )

        message_button = st.button("**:red[Send Message]**")
        if message_button:
            # Execute only if user query is provided
            if not user_query.strip() or all(
                char in string.punctuation for char in user_query.strip()
            ):
                st.error(
                    "❌ Please enter a valid word. The input should not be only **spaces**, **punctuation**, or **empty**."
                )
            else:
                start_time = time.time()
                with st.spinner("Finding similar documents..."):
                    query_pipeline.set_model(selected_embedding_model_name)
                    if num_results != 0:
                        similar_docs = query_pipeline.find_similar_documents(
                            query_text=user_query, num_results=num_results
                        )
                    else:
                        similar_docs = []

                    if not similar_docs:
                        st.error(
                            "❌ User has chosen not to provide documents from the knowledge base!"
                        )
                    else:
                        with st.expander(
                            "Used **:green[Relevent Documents]** in Context",
                            expanded=False,
                        ):
                            for doc in similar_docs:
                                st.info(doc)

                # Prepare context-enhanced prompt
                with st.spinner("Preparing context-enhanced prompt..."):
                    if len(similar_docs) == 0:
                        similar_docs = [
                            "No documents found related to user query! Use your external knowledge or search the internet if possible"
                        ]
                    (
                        context_enhanced_prompt,
                        expertise_area_cost,
                        identified_expertise_area,
                    ) = query_pipeline.determine_expertise_and_prepare_prompt(
                        user_query=user_query,
                        similar_docs=similar_docs,
                        inference_model=selected_llm_name,
                        max_completion_tokens=selected_llm_tokens_limit,
                        temperature=selected_llm_temp,
                    )
                    with st.expander("Expertise Area Identification", expanded=False):
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
                st.chat_message("assistant").write_stream(
                    stream_response(contextual_response)
                )

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
                        | ⏱ **Time Taken** | Total time taken to process the query and generate the response. | **:red[{elapsed_time_formatted}]** |
                        | 💵 **Cost for Determining Expertise Area** | Cost from the initial prompt to determine the expertise area. | **:red[$ {expertise_area_cost:.6f}]** |
                        | 🤑 **Cost to Query the LLM** | Cost estimated based on the processing and querying with the RAG model. | **:red[{formatted_cost}]** |
                        | 🤖 **LLM Model Used** | AI model used for generating the response. | **:green[{selected_llm_name}]** | 
                        """

                    st.markdown(detailed_summary_table, unsafe_allow_html=True)
