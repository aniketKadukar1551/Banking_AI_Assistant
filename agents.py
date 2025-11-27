import re
import os
from tools import AccountTool, TransactionTool, CardTool
from rag_engine import BankRAG

# Optional OpenAI integration
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, query, context=None):
        raise NotImplementedError

class AccountInfoAgent(Agent):
    def __init__(self):
        super().__init__("AccountInfoAgent")
        self.tool = AccountTool()

    def process(self, query, context=None):
        # Simple keyword extraction for demo purposes
        # In a real scenario, an LLM would parse the intent and parameters
        account_id = "123456789" # Default mock ID
        if "balance" in query.lower():
            return self.tool.get_balance(account_id)
        elif "details" in query.lower():
            return self.tool.get_details(account_id)
        return "I can help with account balance and details."

class TransactionAgent(Agent):
    def __init__(self):
        super().__init__("TransactionAgent")
        self.tool = TransactionTool()

    def process(self, query, context=None):
        account_id = "123456789"
        if "recent" in query.lower() or "transactions" in query.lower():
            return self.tool.get_recent_transactions(account_id)
        elif "transfer" in query.lower():
            # Mock parsing
            amount = 100
            target = "987654321"
            return self.tool.transfer_funds(account_id, target, amount)
        return "I can help with transactions and transfers."

class CardServicesAgent(Agent):
    def __init__(self):
        super().__init__("CardServicesAgent")
        self.tool = CardTool()

    def process(self, query, context=None):
        card_last4 = "4321"
        if "block" in query.lower():
            return self.tool.block_card(card_last4)
        elif "replace" in query.lower() or "lost" in query.lower():
            return self.tool.request_replacement(card_last4)
        return "I can help with card blocking and replacement."

class Orchestrator:
    def __init__(self, rag_engine: BankRAG, use_ai=False, api_key=None):
        self.rag = rag_engine
        self.account_agent = AccountInfoAgent()
        self.transaction_agent = TransactionAgent()
        self.card_agent = CardServicesAgent()
        self.use_ai = use_ai and OPENAI_AVAILABLE
        self.ai_client = None
        
        if self.use_ai and api_key:
            try:
                self.ai_client = OpenAI(api_key=api_key)
                print("[Orchestrator] AI Mode enabled")
            except Exception as e:
                print(f"[Orchestrator] Failed to initialize AI: {str(e)}")
                self.use_ai = False

    def _get_ai_response(self, query, context=""):
        """Simple AI response using OpenAI"""
        if not self.ai_client:
            return context
        
        try:
            messages = [
                {"role": "system", "content": "You are a helpful banking assistant. Provide clear, concise answers based on the context provided."},
                {"role": "user", "content": f"Query: {query}\n\nContext: {context}\n\nProvide a helpful response:"}
            ]
            
            response = self.ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"AI service is currently unavailable. Error: {str(e)}"
            print(f"[Orchestrator] {error_msg}")
            return f"I apologize, but I'm having trouble processing your request right now. The AI service is temporarily unavailable. Please try again later or contact support if the issue persists.\n\nError details: {str(e)}"

    def route_query(self, query):
        query_lower = query.lower()
        
        # Check for policy/info questions first (RAG)
        # Keywords: fee, requirement, dispute, policy, how to, what is
        rag_keywords = ["fee", "cost", "charge", "requirement", "document", "id", "dispute", "policy", "process", "how to", "what is"]
        if any(k in query_lower for k in rag_keywords) and not any(k in query_lower for k in ["my account", "my card", "transfer", "block"]):
            print(f"[Orchestrator] Routing to RAG System...")
            result = self.rag.retrieve(query)
            if self.use_ai:
                return self._get_ai_response(query, result)
            return result

        # Check for specific agent actions
        if "account" in query_lower or "balance" in query_lower:
            print(f"[Orchestrator] Routing to AccountInfoAgent...")
            result = self.account_agent.process(query)
            if self.use_ai:
                return self._get_ai_response(query, str(result))
            return result
        
        if "transfer" in query_lower or "transaction" in query_lower or "sent" in query_lower or "received" in query_lower:
            print(f"[Orchestrator] Routing to TransactionAgent...")
            result = self.transaction_agent.process(query)
            if self.use_ai:
                return self._get_ai_response(query, str(result))
            return result
            
        if "card" in query_lower or "block" in query_lower or "lost" in query_lower:
            print(f"[Orchestrator] Routing to CardServicesAgent...")
            result = self.card_agent.process(query)
            if self.use_ai:
                return self._get_ai_response(query, str(result))
            return result

        # Fallback to RAG if unsure, maybe it's a general question
        print(f"[Orchestrator] Unsure of intent, checking Knowledge Base...")
        result = self.rag.retrieve(query)
        if self.use_ai:
            return self._get_ai_response(query, result)
        return result
