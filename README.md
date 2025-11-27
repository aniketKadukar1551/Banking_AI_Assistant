# Banking AI Assistant

A multi-agent banking assistant system with RAG (Retrieval-Augmented Generation) capabilities using Milvus vector database.

## Features

- **Multi-Agent System**: Specialized agents for different banking domains (Account Info, Transactions, Card Services)
- **RAG Engine**: Knowledge retrieval from banking policy documents using Milvus and sentence-transformers
- **Mock Banking APIs**: Simulated account, transaction, and card operations
- **Audit Logging**: Comprehensive logging for compliance and debugging
- **AI Integration**: Optional OpenAI integration for enhanced natural language responses

## Installation

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Generate Data Files

First, generate the mock banking policy PDFs:

```bash
python data_gen.py
```

This creates three PDF files in the `data/` directory:
- `fee_schedule.pdf` - Banking fees information
- `KYC_requirements.pdf` - Know Your Customer requirements
- `dispute_process.pdf` - Transaction dispute procedures

### Step 2: Run the Demo

**Without AI (Rule-based mode):**
```bash
python main.py
```

**With AI (OpenAI integration):**
1. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   USE_AI=true
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

The demo will:
1. Initialize the RAG engine with Milvus
2. Ingest the policy documents
3. Run through several demo scenarios showcasing different capabilities

## Project Structure

```
.
├── agents.py              # Agent classes and orchestrator
├── data_gen.py            # PDF data generation
├── logger.py              # Audit logging system
├── main.py                # Main demo entry point
├── rag_engine.py          # RAG implementation with Milvus
├── tools.py               # Mock banking API tools
├── web_interface.html     # Frontend mockup (not connected)
├── requirements.txt       # Python dependencies
├── data/                  # Generated PDF files
└── milvus_demo.db         # Milvus database (generated)
```

## Components

### RAG Engine (`rag_engine.py`)
- Uses Milvus for vector storage
- Employs sentence-transformers for embeddings
- Handles document ingestion and semantic search

### Agents (`agents.py`)
- **Orchestrator**: Routes queries to appropriate agents or RAG (with optional AI enhancement)
- **AccountInfoAgent**: Handles account balance and details
- **TransactionAgent**: Manages transactions and transfers
- **CardServicesAgent**: Card blocking and replacement

### AI Integration (Optional)
When enabled, the system uses OpenAI GPT-3.5-turbo to:
- Enhance responses with natural language generation
- Provide more conversational and context-aware answers
- Transform technical outputs into user-friendly explanations

### Tools (`tools.py`)
Mock implementations of banking APIs:
- Account operations (balance, details)
- Transaction operations (history, transfers)
- Card operations (block, replace)

### Logger (`logger.py`)
Audit logging for:
- User queries
- Sensitive actions
- RAG retrievals

## Demo Scenarios

The demo runs 5 scenarios:
1. Policy query (RAG) - Wire transfer fees
2. Account action (Mock Tool) - Account balance
3. Complex policy query (RAG) - Dispute process
4. Sensitive action (Mock Tool) - Card blocking
5. Transaction inquiry (Mock Tool) - Recent transactions

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

Key dependencies:
- langchain & langchain-community
- sentence-transformers
- pymilvus
- reportlab (for PDF generation)
- openai (optional, for AI enhancement)
- streamlit (optional, for web interface)
- fastapi (optional, for API endpoints)

## Notes

- The system uses a local Milvus database (`milvus_demo.db`)
- All banking operations are mocked and return simulated data
- The web interface (`web_interface.html`) is a UI mockup and not connected to the backend
- Logs are stored in `banking_assistant.log` and `audit.log`

## Future Enhancements

- Connect web interface to backend
- Add real LLM integration for better intent parsing
- Implement real banking API connections
- Add authentication and authorization
- Deploy as a web service with FastAPI

## License

This is a demo project for educational purposes.
