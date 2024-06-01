import streamlit as st


def about_tab():
    st.header("🔥About :green[Me] & the :red[LLM RAG App]")

    st.markdown(
        """
    #### 🌟 Overview 
    This is a **Streamlit app** leveraging a :red[RAG] (Retrieval-Augmented Generation) :red[LLM] (Large Language Model) with :red[FAISS Vector DB] to offer answers from **uploaded :green[Markdown files]** 📂. The app allows users to upload files, ask questions related to the content of these files, and receive relevant answers generated by the RAG LLM 📚.
    > The source code for this project is available on [GitHub](https://github.com/labrijisaad/LLM-RAG)

    #### ❓ How It Works
    The app consists of the following key areas:

    - **Setup Knowledge Base** 📂: Upload markdown documents to establish the knowledge base.
    - **Explore Knowledge Base** 🔍: Browse and manage the uploaded documents.
    - **RAG Query** 💡: Pose questions to receive answers referencing the knowledge base and the model's knowledge.

    Advanced settings include:
    - **OpenAI Embedding Model Settings**: Select the embedding model for document vectorization.
    - **OpenAI LLM Settings**: Choose the OpenAI language model variant for generating answers.
    - **LLM Temperature**: Adjust the creativity of the model’s responses.
    - **Max Completion Tokens**: Define the maximum length of the generated response.
    - **Drop All Documents in Knowledge Base**: Clear the database by typing a confirmatory command.
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    ### 😄 About Me
    


    - 🌱 I'm **:green[Saad]**, a 24-year-old based in France, with a deep passion for creating projects in the realms of **Data** and **Artificial Intelligence**.
    - 🎓 I hold a **[Data Engineering degree](https://www.inpt.ac.ma/fr/data-engineer)** from INPT.
    - 💼 Currently working as a **:red[Machine Learning Engineering Apprentice]**  at `AXA - Direct Assurance`
    - 📚 I'm also preparing a Master's degree in **[Machine Learning and Data Science](https://biomedicale.u-paris.fr/master-informatique/master-informatique-mlsd/)** at Paris Cité University.

     #### 💼 Work Experience:
    - **:red[Machine Learning Engineer]** Apprenticeship at `AXA - Direct Assurance`, Paris, France (1 year)
    - **:red[Data Engineer / Data Scientist]** Internship at `Chefclub`, Paris, France (6 months)
    - **:red[Data Engineer]** Internship at `Capgemini Engineering`, Casablanca, Morocco (2 months)
    - **:red[Data Scientist]** Internship at `AIOX Labs`, Rabat, Morocco (2 months)
    - **:red[Web/Backend Developer]** Internship at `DXC Technologies`, Rabat, Morocco (2 months)   

    #### 🏅 Certifications: (5x Azure Certified)
    - ![Azure Data Engineer](https://img.shields.io/badge/Azure-Data_Engineer_Associate-blue)
    - ![Azure Data Scientist](https://img.shields.io/badge/Azure-Data_Scientist_Associate-blue)
    - ![Azure Data Fundamentals](https://img.shields.io/badge/Azure-Data_Fundamentals-blue)
    - ![Azure AI Fundamentals](https://img.shields.io/badge/Azure-AI_Fundamentals-blue)
    - ![Azure Fundamentals](https://img.shields.io/badge/Azure-Fundamentals-blue)

    #### 🙌 Connect with Me:
    <div style="text-align: center;">

    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/labrijisaad/)
    [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/labrijisaad)
    
    </div>
    """,
        unsafe_allow_html=True,
    )
