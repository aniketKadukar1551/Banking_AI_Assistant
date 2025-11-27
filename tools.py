class AccountTool:
    def get_balance(self, account_id):
        print(f"[Mock API] Fetching balance for {account_id}")
        return {"account_id": account_id, "balance": 5432.10, "currency": "USD"}

    def get_details(self, account_id):
        print(f"[Mock API] Fetching details for {account_id}")
        return {"account_id": account_id, "type": "Checking", "status": "Active", "owner": "John Doe"}

class TransactionTool:
    def get_recent_transactions(self, account_id, limit=5):
        print(f"[Mock API] Fetching last {limit} transactions for {account_id}")
        return [
            {"date": "2023-10-25", "description": "Grocery Store", "amount": -150.00},
            {"date": "2023-10-24", "description": "Paycheck", "amount": 2500.00},
            {"date": "2023-10-22", "description": "Electric Bill", "amount": -120.50}
        ]

    def transfer_funds(self, source_account, target_account, amount):
        print(f"[Mock API] Transferring ${amount} from {source_account} to {target_account}")
        return {"status": "success", "transaction_id": "TXN998877"}

class CardTool:
    def block_card(self, card_last4, reason="lost"):
        print(f"[Mock API] Blocking card ending in {card_last4}. Reason: {reason}")
        return {"status": "success", "message": f"Card *{card_last4} has been blocked."}

    def request_replacement(self, card_last4):
        print(f"[Mock API] Requesting replacement for card ending in {card_last4}")
        return {"status": "success", "message": "Replacement card shipped. ETA 3-5 business days."}
