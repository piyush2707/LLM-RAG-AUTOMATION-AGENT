# 🤖 LLM-Powered Contextual RAG Agent

## 💡 Project Overview
This project develops an intelligent **Retrieval-Augmented Generation (RAG) agent** designed to provide accurate, context-aware answers and summaries based on a proprietary set of documents (e.g., internal company knowledge base, manuals).

The solution is built with a **production-first MLOps approach**, focusing on automated data ingestion and scalable microservice deployment.

## 🚀 Key Features

* **Contextual Q&A:** Uses RAG architecture to eliminate LLM hallucinations and provide answers grounded in the provided documents.
* **Automated Ingestion Concept:** Implements the logic for automated indexing of new documents (simulating an **n8n/webhook** trigger from a cloud storage event).
* **Scalable API:** Provides a robust, low-latency Q&A endpoint using **FastAPI**.
* **Containerized Deployment:** Ready for cloud orchestration via **Docker** and automated deployment via **CI/CD**.

## 🛠️ Tech Stack & Architecture

| Component | Tool / Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | **LangChain** | Orchestrates the RAG pipeline (Loading, Splitting, Embedding, Retrieval). |
| **API** | **FastAPI** | High-performance Q&A microservice endpoint. |
| **Containerization** | **Docker** | Ensures reproducible and portable deployment. |
| **Vector Store** | **ChromaDB** | Stores document embeddings locally for fast retrieval. |
| **MLOps Concept** | **GitHub Actions** | CI/CD pipeline definition for automated builds. |
| **Core Languages** | Python, YAML | Application logic and configuration. |

## ⚙️ MLOps & Deployment Highlights

1.  **Ingestion Pipeline (`ingestion.py`):** New PDF documents are processed, text is extracted, embeddings are generated, and the Vector Store is updated.
2.  **RAG Endpoint (`api.py`):** The Q&A logic is exposed via a single `/query` POST endpoint in FastAPI.
3.  **Reproducibility:** The entire application stack is containerized using the **`Dockerfile`**.
4.  **Continuous Integration:** (Conceptual) A GitHub Actions workflow (`.github/workflows/ci_cd.yml`) would define the process to automatically build and push the Docker image upon code changes.

## 🏃 Getting Started

### Prerequisites
* Python 3.10+
* Docker (Optional, for production deployment)
* **OpenAI API Key** (Set as `OPENAI_API_KEY` in your local `.env` file)

### Local Setup

1.  **Clone the repository:** `git clone https://github.com/piyush2707/LLM-RAG-Automation-Agent`
2.  **Install dependencies:** `pip install -r requirements.txt`
3.  **Add Document:** Place your PDF documents (e.g., `sample_doc.pdf`) inside the `data/` folder.
4.  **Run Ingestion:** Run the ingestion script once to create the vector database:
    ```bash
    python src/ingestion.py
    ```
5.  **Run API Locally (Development):**
    ```bash
    uvicorn src.api:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

---
*Created by Piyush Joshi | Connect on [LinkedIn](https://www.linkedin.com/in/piyush2707/)*
