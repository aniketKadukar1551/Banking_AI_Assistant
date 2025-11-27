import os
from openai import OpenAI
from tools import AccountTool, TransactionTool, CardTool
from rag_engine import BankRAG

# Prompt Templates
ACCOUNT_PROMPT = """You are a banking account specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""

TRANSACTION_PROMPT = """You are a banking transaction specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""

CARD_PROMPT = """You are a banking card services specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""

RAG_PROMPT = """You are a banking policy expert. Based on the knowledge base information, provide a clear and professional response to the user's query.

User Query: {query}
Knowledge Base: {context}

Response:"""

class Agent:
    """Base Agent class with LLM integration"""
    
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm  # LLM component
        self.memory = []  # Memory component (conversation history)

    def process(self, query):
        raise NotImplementedError
    
    def _execute_with_llm(self, prompt):
        """Execute LLM call and return result"""
        try:
            response = self.llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            result = response.choices[0].message.content
            self.memory.append({"query": prompt, "response": result})
            return result
        except Exception as e:
            return f"Error: Unable to process your request. {str(e)}"

class AccountInfoAgent(Agent):
    def __init__(self, llm):
        super().__init__("AccountInfoAgent", llm)
        self.tool = AccountTool()  # Tool component

    def process(self, query):
        # 1. Load tool and execute
        account_id = "123456789"
        if "balance" in query.lower():
            tool_result = self.tool.get_balance(account_id)
        elif "details" in query.lower():
            tool_result = self.tool.get_details(account_id)
        else:
            tool_result = "I can help with account balance and details."
        
        # 2. Define prompt with tool result
        prompt = ACCOUNT_PROMPT.format(query=query, tool_result=str(tool_result))
        
        # 3. Execute LLM call and return agent result
        return self._execute_with_llm(prompt)

class TransactionAgent(Agent):
    def __init__(self, llm):
        super().__init__("TransactionAgent", llm)
        self.tool = TransactionTool()  # Tool component

    def process(self, query):
        # 1. Load tool and execute
        account_id = "123456789"
        if "recent" in query.lower() or "transactions" in query.lower():
            tool_result = self.tool.get_recent_transactions(account_id)
        elif "transfer" in query.lower():
            amount = 100
            target = "987654321"
            tool_result = self.tool.transfer_funds(account_id, target, amount)
        else:
            tool_result = "I can help with transactions and transfers."
        
        # 2. Define prompt with tool result
        prompt = TRANSACTION_PROMPT.format(query=query, tool_result=str(tool_result))
        
        # 3. Execute LLM call and return agent result
        return self._execute_with_llm(prompt)

class CardServicesAgent(Agent):
    def __init__(self, llm):
        super().__init__("CardServicesAgent", llm)
        self.tool = CardTool()  # Tool component

    def process(self, query):
        # 1. Load tool and execute
        card_last4 = "4321"
        if "block" in query.lower():
            tool_result = self.tool.block_card(card_last4)
        elif "replace" in query.lower() or "lost" in query.lower():
            tool_result = self.tool.request_replacement(card_last4)
        else:
            tool_result = "I can help with card blocking and replacement."
        
        # 2. Define prompt with tool result
        prompt = CARD_PROMPT.format(query=query, tool_result=str(tool_result))
        
        # 3. Execute LLM call and return agent result
        return self._execute_with_llm(prompt)

class Orchestrator:
    def __init__(self, rag_engine: BankRAG, api_key):
        self.rag = rag_engine
        # Initialize LLM (AI configuration already validated in main.py)
        self.llm = OpenAI(api_key=api_key)
        
        # Initialize agents with LLM
        self.account_agent = AccountInfoAgent(self.llm)
        self.transaction_agent = TransactionAgent(self.llm)
        self.card_agent = CardServicesAgent(self.llm)
        
        print("[Orchestrator] AI-powered agents initialized successfully")

    def _process_rag_query(self, query, context):
        """Process RAG query with LLM"""
        try:
            prompt = RAG_PROMPT.format(query=query, context=context)
            response = self.llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: Unable to process your request. {str(e)}"

    def route_query(self, query):
        """Route query to appropriate agent and return agent result"""
        query_lower = query.lower()
        
        # Check for policy/info questions (RAG)
        rag_keywords = ["fee", "cost", "charge", "requirement", "document", "id", "dispute", "policy", "process", "how to", "what is"]
        if any(k in query_lower for k in rag_keywords) and not any(k in query_lower for k in ["my account", "my card", "transfer", "block"]):
            print(f"[Orchestrator] Routing to RAG System...")
            context = self.rag.retrieve(query)
            return self._process_rag_query(query, context)

        # Route to specific agents
        if "account" in query_lower or "balance" in query_lower:
            print(f"[Orchestrator] Routing to AccountInfoAgent...")
            return self.account_agent.process(query)
        
        if "transfer" in query_lower or "transaction" in query_lower or "sent" in query_lower or "received" in query_lower:
            print(f"[Orchestrator] Routing to TransactionAgent...")
            return self.transaction_agent.process(query)
            
        if "card" in query_lower or "block" in query_lower or "lost" in query_lower:
            print(f"[Orchestrator] Routing to CardServicesAgent...")
            return self.card_agent.process(query)

        # Fallback to RAG
        print(f"[Orchestrator] Unsure of intent, checking Knowledge Base...")
        context = self.rag.retrieve(query)
        return self._process_rag_query(query, context)
