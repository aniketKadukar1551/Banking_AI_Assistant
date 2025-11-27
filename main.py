import os
import time
from rag_engine import BankRAG
from agents import Orchestrator
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Banking AI Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI components on startup"""
    global orchestrator
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[API] WARNING: OPENAI_API_KEY not set. API will return errors.")
        return
    
    print("[API] Initializing RAG Engine...")
    rag = BankRAG()
    
    data_files = ["data/fee_schedule.pdf", "data/KYC_requirements.pdf", "data/dispute_process.pdf"]
    if all(os.path.exists(f) for f in data_files):
        rag.ingest_docs(data_files)
        orchestrator = Orchestrator(rag, api_key)
        print("[API] AI Assistant initialized successfully")
    else:
        print("[API] WARNING: Data files not found. Run data_gen.py first.")

@app.get("/")
async def root():
    """Serve the HTML frontend"""
    try:
        with open("web_interface.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return JSONResponse({"error": "Frontend not found"}, status_code=404)

@app.post("/api/ask")
async def ask_question(request: Request):
    """Main endpoint for AI queries"""
    if orchestrator is None:
        return JSONResponse({
            "error": "AI service not configured. Please set OPENAI_API_KEY and ensure data files exist."
        }, status_code=503)
    
    try:
        data = await request.json()
        query = data.get("query", "").strip()
        
        if not query:
            return JSONResponse({"error": "Query cannot be empty"}, status_code=400)
        
        # Route query through orchestrator
        response = orchestrator.route_query(query)
        
        return JSONResponse({
            "response": response,
            "status": "success"
        })
    
    except Exception as e:
        return JSONResponse({
            "error": f"Failed to process query: {str(e)}"
        }, status_code=500)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy" if orchestrator else "not_initialized",
        "ai_enabled": orchestrator is not None
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy" if orchestrator else "not_initialized",
        "ai_enabled": orchestrator is not None
    })

def main():
    """CLI Demo Mode"""
    print("="*50)
    print("Banking Support AI Assistant + Milvus RAG Demo")
    print("="*50)

    # Check for AI configuration (strict requirement)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\n[System] ERROR: AI configuration missing!")
        print("[System] This assistant requires AI to function.")
        print("[System] Please set OPENAI_API_KEY in your environment:")
        print("         export OPENAI_API_KEY=your_api_key_here")
        print("         or create a .env file with OPENAI_API_KEY=your_api_key_here")
        print("\n[System] Exiting...")
        return

    print("\n[System] AI Mode: ENABLED")

    # 1. Initialize RAG and Ingest Data
    print("[System] Initializing RAG Engine...")
    rag = BankRAG()
    
    # Check if data exists, if not wait (assuming data_gen runs separately or we run it here)
    data_files = ["data/fee_schedule.pdf", "data/KYC_requirements.pdf", "data/dispute_process.pdf"]
    if not all(os.path.exists(f) for f in data_files):
        print("[System] Data files not found. Please run data_gen.py first.")
        return

    rag.ingest_docs(data_files)
    print("[System] RAG Initialization Complete.")

    # 2. Initialize Orchestrator with AI
    orchestrator_cli = Orchestrator(rag, api_key)

    # 3. Demo Scenarios
    scenarios = [
        {
            "description": "Scenario 1: Policy Query (RAG)",
            "query": "What is the fee for an international wire transfer?"
        },
        {
            "description": "Scenario 2: Account Action (Mock Tool)",
            "query": "What is my current account balance?"
        },
        {
            "description": "Scenario 3: Complex Policy Query (RAG)",
            "query": "How do I dispute a transaction and how long does it take?"
        },
        {
            "description": "Scenario 4: Sensitive Action (Mock Tool)",
            "query": "I lost my card, please block it immediately."
        },
        {
            "description": "Scenario 5: Transaction Inquiry (Mock Tool)",
            "query": "Show me my recent transactions."
        }
    ]

    print("\n" + "="*50)
    print("Starting Demo Interactions")
    print("="*50)

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- {scenario['description']} ---")
        print(f"User: {scenario['query']}")
        print("Agent processing...")
        time.sleep(1) # Simulate thinking
        response = orchestrator_cli.route_query(scenario['query'])
        print(f"Agent Response:\n{response}")
        print("-" * 30)

if __name__ == "__main__":
    import sys
    
    # Check if running as API server or CLI demo
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        print("Starting API Server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main()
