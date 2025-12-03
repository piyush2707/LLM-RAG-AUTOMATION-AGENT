import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VECTOR_DB_PATH = "vector_store"
# Assumes you place the document in a subfolder named 'data'
DOCUMENTS_PATH = "data/sample_doc.pdf" 

def create_sample_pdf_if_not_exists():
    """Creates a dummy file path for the ingestion script to find."""
    data_dir = "data"
    # Ensure the data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Create a placeholder file if the actual PDF is missing
    if not os.path.exists(DOCUMENTS_PATH):
        print(f"--- WARNING: Placeholder created at {DOCUMENTS_PATH} ---")
        print("Please replace this file with a real PDF document for full functionality.")
        # Create a basic text file disguised as a PDF for testing the file path logic
        with open(DOCUMENTS_PATH, "w") as f:
            f.write("This is a sample document about MLOps, RAG architecture, and Python deployment. It is used to test the ingestion pipeline.")

def run_ingestion():
    """Loads, splits, and embeds documents into the ChromaDB vector store."""
    
    # Check for API key before processing
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env. Cannot run ingestion without API access.")
        return

    # Ensure sample document path exists
    create_sample_pdf_if_not_exists()
    
    # 1. Load documents
    print(f"Loading document from {DOCUMENTS_PATH}...")
    try:
        loader = PyPDFLoader(DOCUMENTS_PATH)
        data = loader.load()
    except Exception as e:
        print(f"Error loading document: {e}")
        return
    
    # 2. Split documents (Chunking)
    # This splitter is good for code and general text.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    docs = text_splitter.split_documents(data)
    print(f"Loaded {len(data)} pages, split into {len(docs)} chunks.")

    # 3. Create Embeddings and Vector Store
    print("Creating embeddings and persisting to ChromaDB...")
    embeddings = OpenAIEmbeddings()
    
    # Create the vector store and persist it
    # This automatically saves the database to the 'vector_store' directory
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=VECTOR_DB_PATH
    )
    vectorstore.persist()
    print(f"✅ Ingestion complete. Vector store saved at {VECTOR_DB_PATH}")

if __name__ == "__main__":
    run_ingestion()

# End of file: ingestion.py
