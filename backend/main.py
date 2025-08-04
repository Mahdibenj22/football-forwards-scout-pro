from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_system import FootballRAGSystem

app = FastAPI(title="Football RAG API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    sources: list = []

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup"""
    global rag_system
    try:
        rag_system = FootballRAGSystem()
        await rag_system.initialize()
        print("🚀 Football RAG System initialized!")
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        raise

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Football RAG API is running",
        "rag_ready": rag_system is not None
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        response = await rag_system.process_query(request.query)
        return QueryResponse(
            response=response["answer"],
            sources=response.get("sources", [])
        )
    except Exception as e:
        print(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Football RAG API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
