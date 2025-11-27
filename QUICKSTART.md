# Quick Start Guide

## Installation & Running

### Option 1: Quick Start Script (Recommended)

```bash
./run.sh
```

This script will:
- Create virtual environment (if needed)
- Install all dependencies
- Generate data files
- Run the demo

### Option 2: Manual Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate data
python data_gen.py

# Run CLI demo
python main.py

# OR run API server
python main.py --api
```

## Running Modes

### 1. CLI Demo Mode (Default)
```bash
python main.py
```
Runs 5 demo scenarios in the terminal.

### 2. Web API Mode (with Frontend)
```bash
python main.py --api
```
Starts the FastAPI server on `http://localhost:8000`

- **Web Interface**: Open browser to `http://localhost:8000`
- **API Endpoint**: `POST http://localhost:8000/api/ask`
- **Health Check**: `GET http://localhost:8000/api/health`

#### API Usage Example:
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my account balance?"}'
```

Response:
```json
{
  "response": "Your current account balance is $5,432.10 USD...",
  "status": "success"
}
```

## What to Expect

The demo will show 5 scenarios:

1. **Policy Query (RAG)**: "What is the fee for an international wire transfer?"
   - System retrieves answer from PDF documents using vector search

2. **Account Action**: "What is my current account balance?"
   - System routes to AccountInfoAgent which uses mock API

3. **Complex Policy Query (RAG)**: "How do I dispute a transaction and how long does it take?"
   - System retrieves detailed policy information

4. **Sensitive Action**: "I lost my card, please block it immediately."
   - System routes to CardServicesAgent for card blocking

5. **Transaction Inquiry**: "Show me my recent transactions."
   - System routes to TransactionAgent for transaction history

## Installed Packages

All required packages are installed in the virtual environment:

✅ **Core AI/ML**:
- langchain (1.1.0) - LLM framework
- langchain-community (0.4.1) - Community integrations
- sentence-transformers (5.1.2) - Text embeddings
- pymilvus (2.6.4) - Vector database

✅ **Web Frameworks** (for future extensions):
- streamlit (1.51.0) - Web UI framework
- fastapi (0.122.0) - API framework

✅ **Development Tools**:
- pytest (9.0.1) - Testing framework
- black (25.11.0) - Code formatter
- flake8 (7.3.0) - Linter

## Project Files

- `main.py` - Run this to start the demo
- `data_gen.py` - Generates sample PDF files
- `rag_engine.py` - Vector search implementation
- `agents.py` - Multi-agent orchestration
- `tools.py` - Mock banking APIs
- `logger.py` - Audit logging

## Output Files

After running, you'll find:
- `data/` - Generated PDF documents
- `milvus_demo.db` - Vector database
- `banking_assistant.log` - Application logs
- `audit.log` - Audit trail logs

## Troubleshooting

**Issue**: "externally-managed-environment" error
- **Solution**: Make sure you've activated the virtual environment: `source venv/bin/activate`

**Issue**: No data files found
- **Solution**: Run `python data_gen.py` first

**Issue**: Import errors
- **Solution**: Reinstall packages: `pip install -r requirements.txt`

## Next Steps

1. Review the code to understand the architecture
2. Modify the scenarios in `main.py` to test different queries
3. Extend the agents with new capabilities
4. Connect the web interface (`web_interface.html`) to the backend
5. Integrate real LLMs (OpenAI, Anthropic, etc.)
