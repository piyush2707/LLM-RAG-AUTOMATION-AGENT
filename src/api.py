from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .core_rag import query_rag_agent # Import the core RAG function

# Initialize FastAPI app
app = FastAPI(
    title="LLM RAG Automation Agent API",
    description="Microservice for contextual Q&A using RAG architecture.",
    version="1.0.0"
)

# Pydantic model for request body
# This defines the expected input format for the API
class QueryRequest(BaseModel):
    query: str
    
# Root endpoint for health check
@app.get("/")
def read_root():
    """Returns the API status for health monitoring."""
    return {"status": "ok", "message": "RAG Agent API is running."}

# Main Q&A endpoint
@app.post("/query")
def query_agent(request: QueryRequest):
    """
    Endpoint to send a question to the RAG agent and get a contextual answer.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    print(f"Received query: {request.query}")
    
    # Call the RAG function from core_rag.py
    response = query_rag_agent(request.query)
    
    # Handle errors returned from the core RAG logic (e.g., FileNotFoundError)
    if "error" in response:
        # 404 for missing vector store, 500 for other server errors
        status_code = 404 if "not found" in response["error"] else 500
        raise HTTPException(status_code=status_code, detail=response["error"])
        
    # Return the clean, structured response
    return {
        "question": request.query,
        "answer": response["answer"],
        "sources": response["source_documents"]
    }

# End of file: api.py
