from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from tools import AccountTool, TransactionTool, CardTool
from rag_engine import BankRAG

# Prompt Templates using modern ChatPromptTemplate
account_prompt = ChatPromptTemplate.from_template(
    """You are a banking account specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""
)

transaction_prompt = ChatPromptTemplate.from_template(
    """You are a banking transaction specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""
)

card_prompt = ChatPromptTemplate.from_template(
    """You are a banking card services specialist. Based on the tool result, provide a clear and professional response to the user's query.

User Query: {query}
Tool Result: {tool_result}

Response:"""
)

rag_prompt = ChatPromptTemplate.from_template(
    """You are a banking policy expert. Based on the knowledge base information, provide a clear and professional response to the user's query.

User Query: {query}
Knowledge Base: {context}

Response:"""
)

class Agent:
    """Base Agent class with LangChain LCEL Chain"""
    def __init__(self, name, llm, prompt_template):
        self.name = name
        self.llm = llm
        self.prompt = prompt_template
        self.output_parser = StrOutputParser()
        # Message history for conversation memory
        self.message_history = ChatMessageHistory()
        # Create chain using LCEL (LangChain Expression Language)
        self.chain = self.prompt | self.llm | self.output_parser

    def process(self, query):
        raise NotImplementedError

class AccountInfoAgent(Agent):
    def __init__(self, llm):
        super().__init__("AccountInfoAgent", llm, account_prompt)
        self.tool = AccountTool()

    def process(self, query):
        account_id = "123456789"
        if "balance" in query.lower():
            tool_result = self.tool.get_balance(account_id)
        elif "details" in query.lower():
            tool_result = self.tool.get_details(account_id)
        else:
            tool_result = "I can help with account balance and details."
        # Use invoke with dict for LCEL chains
        response = self.chain.invoke({"query": query, "tool_result": str(tool_result)})
        # Save to message history
        self.message_history.add_user_message(query)
        self.message_history.add_ai_message(response)
        return response

class TransactionAgent(Agent):
    def __init__(self, llm):
        super().__init__("TransactionAgent", llm, transaction_prompt)
        self.tool = TransactionTool()

    def process(self, query):
        account_id = "123456789"
        if "recent" in query.lower() or "transactions" in query.lower():
            tool_result = self.tool.get_recent_transactions(account_id)
        elif "transfer" in query.lower():
            amount = 100
            target = "987654321"
            tool_result = self.tool.transfer_funds(account_id, target, amount)
        else:
            tool_result = "I can help with transactions and transfers."
        # Use invoke with dict for LCEL chains
        response = self.chain.invoke({"query": query, "tool_result": str(tool_result)})
        # Save to message history
        self.message_history.add_user_message(query)
        self.message_history.add_ai_message(response)
        return response

class CardServicesAgent(Agent):
    def __init__(self, llm):
        super().__init__("CardServicesAgent", llm, card_prompt)
        self.tool = CardTool()

    def process(self, query):
        card_last4 = "4321"
        if "block" in query.lower():
            tool_result = self.tool.block_card(card_last4)
        elif "replace" in query.lower() or "lost" in query.lower():
            tool_result = self.tool.request_replacement(card_last4)
        else:
            tool_result = "I can help with card blocking and replacement."
        # Use invoke with dict for LCEL chains
        response = self.chain.invoke({"query": query, "tool_result": str(tool_result)})
        # Save to message history
        self.message_history.add_user_message(query)
        self.message_history.add_ai_message(response)
        return response

class Orchestrator:
    def __init__(self, rag_engine: BankRAG, api_key):
        self.rag = rag_engine
        # Initialize LangChain LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=api_key,
            temperature=0.7
        )
        # Initialize agents with LLM
        self.account_agent = AccountInfoAgent(self.llm)
        self.transaction_agent = TransactionAgent(self.llm)
        self.card_agent = CardServicesAgent(self.llm)
        # RAG chain using LCEL
        output_parser = StrOutputParser()
        self.rag_chain = rag_prompt | self.llm | output_parser
        print("[Orchestrator] LangChain-powered agents initialized successfully")

    def _process_rag_query(self, query, context):
        """Process RAG query with LLM Chain"""
        response = self.rag_chain.invoke({"query": query, "context": context})
        return response

    def route_query(self, query):
        """Route query to appropriate agent chain"""
        query_lower = query.lower()
        # Check for policy/info questions (RAG)
        rag_keywords = ["fee", "cost", "charge", "requirement", "document", "id", "dispute", "policy", "process", "how to", "what is"]
        if any(k in query_lower for k in rag_keywords) and not any(k in query_lower for k in ["my account", "my card", "transfer", "block"]):
            print(f"[Orchestrator] Routing to RAG Chain...")
            context = self.rag.retrieve(query)
            return self._process_rag_query(query, context)
        # Route to specific agent chains
        if "account" in query_lower or "balance" in query_lower:
            print(f"[Orchestrator] Routing to AccountInfoAgent Chain...")
            return self.account_agent.process(query)
        if "transfer" in query_lower or "transaction" in query_lower or "sent" in query_lower or "received" in query_lower:
            print(f"[Orchestrator] Routing to TransactionAgent Chain...")
            return self.transaction_agent.process(query)
        if "card" in query_lower or "block" in query_lower or "lost" in query_lower:
            print(f"[Orchestrator] Routing to CardServicesAgent Chain...")
            return self.card_agent.process(query)
        # Fallback to RAG chain
        print(f"[Orchestrator] Unsure of intent, checking Knowledge Base Chain...")
        context = self.rag.retrieve(query)
        return self._process_rag_query(query, context)
