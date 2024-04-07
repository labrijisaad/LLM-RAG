# LLM RAG ( Ongoing Project 🚧 )

## System Architecture
The following diagram illustrates the flow of data through the system:

```mermaid
graph TD
    A[User Files] -->|Read & Process| B[Semantic Database Setup]
    B -->|Generate Embeddings & FAISS Index| C[Vector Store]
    C -->|Utilize OpenAI's Models| D[Semantic Search]
    E[User Query] -->|Vectorization| D
    D -->|Select Top Documents| F[Top Documents]
    F -->|Include Selected Docs in Context| G[Contextualized Documents]
    E -->|Determine Expertise using OpenAI| H[Expertise Area]
    H -->|Formulate Prompt| I[Prompt with Context]
    G --> I
    I -->|Query OpenAI LLM| J[LLM Response]
    J -->|Generate Answer| K[Answer]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
    style I fill:#fbb,stroke:#333,stroke-width:2px
    style J fill:#fbb,stroke:#333,stroke-width:2px
    style K fill:#fbb,stroke:#333,stroke-width:2px
```

## Connect with me 🌐
<div align="center">
  <a href="https://www.linkedin.com/in/labrijisaad/">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" style="margin-bottom: 5px;"/>
  </a>
  <a href="https://github.com/labrijisaad">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" style="margin-bottom: 5px;"/>
  </a>
</div>