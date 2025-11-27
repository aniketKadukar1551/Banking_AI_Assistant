import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('banking_assistant.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('BankingAssistant')

class AuditLogger:
    """Logs all banking operations for compliance and security"""
    
    def __init__(self, log_file='audit.log'):
        self.audit_logger = logging.getLogger('Audit')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        ))
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)
    
    def log_query(self, query_type, query, user_id='anonymous'):
        """Log user queries"""
        self.audit_logger.info(
            f"USER_QUERY | User: {user_id} | Type: {query_type} | Query: {query}"
        )
    
    def log_action(self, action_type, details, user_id='anonymous'):
        """Log sensitive actions"""
        self.audit_logger.info(
            f"ACTION | User: {user_id} | Type: {action_type} | Details: {details}"
        )
    
    def log_rag_retrieval(self, query, sources, user_id='anonymous'):
        """Log RAG retrievals"""
        self.audit_logger.info(
            f"RAG_RETRIEVAL | User: {user_id} | Query: {query} | Sources: {sources}"
        )

# Create global audit logger instance
audit_logger = AuditLogger()
