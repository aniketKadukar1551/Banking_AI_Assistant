import os
import time
from rag_engine import BankRAG
from agents import Orchestrator

def main():
    print("="*50)
    print("Banking Support AI Assistant + Milvus RAG Demo")
    print("="*50)

    # Check for AI configuration
    use_ai = os.getenv("USE_AI", "false").lower() == "true"
    api_key = os.getenv("OPENAI_API_KEY")
    
    if use_ai and api_key:
        print("\n[System] AI Mode: ENABLED")
    else:
        print("\n[System] AI Mode: DISABLED (set USE_AI=true and OPENAI_API_KEY to enable)")
        use_ai = False

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

    # 2. Initialize Orchestrator with optional AI
    orchestrator = Orchestrator(rag, use_ai=use_ai, api_key=api_key)

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
        response = orchestrator.route_query(scenario['query'])
        print(f"Agent Response:\n{response}")
        print("-" * 30)

if __name__ == "__main__":
    main()
