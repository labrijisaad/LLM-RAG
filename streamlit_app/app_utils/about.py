import streamlit as st


def about_tab():
    st.header("🔥About :green[Me] & the :red[LLM RAG App]")

    st.markdown(
        """
    #### 🌟 Overview 
    This is a **Streamlit app** leveraging a :red[RAG] (Retrieval-Augmented Generation) :red[LLM] (Large Language Model) with :red[FAISS Vector DB] to offer answers from **uploaded :green[Markdown files]** 📂. The app allows users to upload files, ask questions related to the content of these files, and receive relevant answers generated by the RAG LLM 📚.
    > The source code for this project is available on [GitHub](https://github.com/labrijisaad/LLM-RAG)

    #### ❓How It Works
    The LLM RAG Streamlit app is structured into several key areas, each serving a specific function within the application:


    -  **`Setup Knowledge Base`** 📂: Users can establish their **knowledge base** by uploading **markdown documents**. This forms the foundational data that the app will reference for generating answers.

    -  **`Explore Knowledge Base`** 🔍: After setting up the knowledge base, users can browse and manage the uploaded documents. This allows users to ensure that the data is ready for queries.

    -  **`RAG Query`** 💡: In this tab, users can pose questions that the app will answer by referencing the content within the knowledge base. The RAG (Retrieval-Augmented Generation) model utilizes both the uploaded documents and the model's own knowledge to generate responses.

    Additionally, the app offers advanced settings to tailor the querying experience:

    - **`OpenAI Embedding Model Settings`**: Users select the desired embedding model for document vectorization. Choices affect the precision of semantic search and the cost per token processed.
    
    - **`OpenAI LLM Settings`**: This setting allows users to choose the specific OpenAI language model variant for generating answers. It also displays the associated costs for input and output processing per 1,000 tokens.

    - **`LLM Temperature`**: Adjusting this parameter influences the creativity of the language model’s responses. A higher temperature may yield more varied and creative outputs, while a lower temperature results in more deterministic and conservative text.

    - **`Max Completion Tokens`**: Users can define the maximum length of the generated response by setting the maximum number of tokens (words and characters) the model should produce.

    - **Drop All Documents in `Knowledge Base`**: This functionality is crucial for managing the knowledge base. If users need to clear the database, they can do so by typing a confirmatory command.
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    ### 😄 About Me
    

    <p align="center">
       <img src="https://github.com/labrijisaad/LLM-RAG/assets/74627083/6e0b512d-6dca-49f0-84f0-af45bce3380d" width="20%" />
    </p>


    - 🌱 I'm **:green[Saad]**, a 23-year-old based in France, with a deep passion for creating projects in the realms of **Data** and **Artificial Intelligence**.
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
