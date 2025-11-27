import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_DIR = "data"

def create_pdf(filename, content):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, filename.replace(".pdf", "").replace("_", " ").title())
    
    c.setFont("Helvetica", 12)
    y_position = height - 80
    
    for line in content.split('\n'):
        if y_position < 50:
            c.showPage()
            y_position = height - 50
        c.drawString(50, y_position, line)
        y_position -= 15
        
    c.save()
    print(f"Generated {filepath}")

def generate_data():
    fee_schedule_content = """
    Standard Checking Account Fees:
    - Monthly Maintenance Fee: $12.00 (waived with $1,500 min daily balance)
    - Overdraft Fee: $35.00 per item
    - ATM Fee (Non-Network): $2.50 per transaction
    
    Savings Account Fees:
    - Excessive Withdrawal Fee: $5.00 per withdrawal over 6 per month
    
    Wire Transfers:
    - Domestic Incoming: $15.00
    - Domestic Outgoing: $30.00
    - International Incoming: $16.00
    - International Outgoing: $45.00
    """
    
    kyc_requirements_content = """
    Know Your Customer (KYC) Requirements:
    
    To open a new account, you must provide:
    1. Valid Government-Issued Photo ID (Driver's License, Passport, State ID)
    2. Proof of Address (Utility bill, Bank statement, Lease agreement - dated within last 60 days)
    3. Social Security Number (SSN) or ITIN
    
    For Business Accounts:
    - Articles of Incorporation
    - EIN (Employer Identification Number)
    - Beneficial Ownership Information
    """
    
    dispute_process_content = """
    Transaction Dispute Process:
    
    1. Notification: You must notify the bank within 60 days of the statement date where the error appeared.
    2. Provisional Credit: We will provide provisional credit within 10 business days while we investigate.
    3. Investigation: Investigations typically take 45-90 days depending on the transaction type.
    4. Resolution: You will be notified in writing of the outcome. If the dispute is valid, the credit becomes permanent.
    
    To initiate a dispute, call customer service or use the mobile app 'Dispute' feature.
    """
    
    create_pdf("fee_schedule.pdf", fee_schedule_content)
    create_pdf("KYC_requirements.pdf", kyc_requirements_content)
    create_pdf("dispute_process.pdf", dispute_process_content)

if __name__ == "__main__":
    generate_data()
