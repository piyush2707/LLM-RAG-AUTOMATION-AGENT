import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables (like OPENAI_API_KEY)
load_dotenv()

# Define paths
VECTOR_DB_PATH = "vector_store"

def get_rag_chain():
    """Initializes and returns the RAG retrieval chain."""
    
    # 1. Initialize Embeddings and LLM
    # Assumes OPENAI_API_KEY is set in your .env file
    embeddings = OpenAIEmbeddings()
    
    # Using a fast and capable model
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    # 2. Load Vector Store
    # This checks if the database exists (i.e., if ingestion has been run)
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(f"Vector store not found at '{VECTOR_DB_PATH}'. Please run ingestion.py first.")
        
    vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
    
    # 3. Create RAG Chain
    # RetrievalQA chain combines the LLM with the vector store retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # The 'stuff' method stuffs all retrieved context into the prompt
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}), # Retrieve top 3 relevant chunks
        return_source_documents=True # Important for showing where the answer came from
    )
    
    return qa_chain

# Function to be called by the FastAPI endpoint
def query_rag_agent(question: str):
    """Takes a question, executes the RAG chain, and returns the response."""
    try:
        qa_chain = get_rag_chain()
        # Execute the chain
        result = qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": [doc.metadata.get('source', 'N/A') for doc in result.get("source_documents", [])]
        }
    except FileNotFoundError as e:
        # Pass the error message back to the API
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# End of file: core_rag.py
