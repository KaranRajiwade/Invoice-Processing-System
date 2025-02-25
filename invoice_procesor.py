import mailparser
import pdfplumber
import re
import sqlite3

# Database setup
DATABASE = "invoices.db"

def initialize_db():
    """Create the SQLite database and invoices table if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            invoice_date TEXT,
            supplier TEXT,
            customer TEXT,
            billing_address TEXT,
            shipping_address TEXT,
            supplier_gstin TEXT,
            customer_gstin TEXT,
            subtotal TEXT,
            tax TEXT,
            total TEXT
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

# Load and parse the email file
email_file = "invoice_email.eml"
mail = mailparser.parse_from_file(email_file)

# Extract email details
sender = mail.from_[0]
receiver = mail.to[0]
subject = mail.subject

# Print extracted email details
print(f"Sender: {sender}")
print(f"Receiver: {receiver}")
print(f"Subject: {subject}")

# Skip attachment extraction because the email does not contain one
pdf_file = "invoice.pdf"  # Assuming it's manually placed in the folder

# Extract data from PDF
with pdfplumber.open(pdf_file) as pdf:
    pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Extract details using regex
invoice_number = re.search(r"Invoice Number:\s*(\S+)", pdf_text).group(1)
invoice_date = re.search(r"Invoice Date:\s*([\d-]+)", pdf_text).group(1)
supplier = re.search(r"Supplier:\s*(.+)", pdf_text).group(1)
customer = re.search(r"Customer:\s*(.+)", pdf_text).group(1)
billing_address = re.search(r"Billing Address:\s*(.+)", pdf_text).group(1)
shipping_address = re.search(r"Shipping Address:\s*(.+)", pdf_text).group(1)
supplier_gstin = re.search(r"Supplier GSTIN:\s*(\S+)", pdf_text).group(1)
customer_gstin = re.search(r"Customer GSTIN:\s*(\S+)", pdf_text).group(1)

# Extract item details
items = re.findall(r"(\w+)\s+(\d+)\s+\$(\d+\.\d{2})\s+\$(\d+\.\d{2})", pdf_text)

# Extract amounts
subtotal = re.search(r"Subtotal:\s*\$(\d+\.\d{2})", pdf_text).group(1)
tax = re.search(r"Tax\s*\(\d+%\):\s*\$(\d+\.\d{2})", pdf_text).group(1)
total = re.search(r"Total Amount:\s*\$(\d+\.\d{2})", pdf_text).group(1)

# Print extracted data
print(f"\nExtracted Invoice Data:")
print(f"Invoice Number: {invoice_number}")
print(f"Invoice Date: {invoice_date}")
print(f"Supplier: {supplier}")
print(f"Customer: {customer}")
print(f"Billing Address: {billing_address}")
print(f"Shipping Address: {shipping_address}")
print(f"Supplier GSTIN: {supplier_gstin}")
print(f"Customer GSTIN: {customer_gstin}")
print("Items:")
for item in items:
    print(f" - {item[0]} | Qty: {item[1]} | Price: ${item[2]} | Total: ${item[3]}")
print(f"Subtotal: ${subtotal}")
print(f"Tax: ${tax}")
print(f"Total: ${total}")

# Save extracted invoice data to database
def save_invoice_to_db(invoice_data):
    """Insert extracted invoice data into the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO invoices (invoice_number, invoice_date, supplier, customer, billing_address, shipping_address, 
                              supplier_gstin, customer_gstin, subtotal, tax, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (invoice_data["invoice_number"], invoice_data["invoice_date"], invoice_data["supplier"], 
          invoice_data["customer"], invoice_data["billing_address"], invoice_data["shipping_address"], 
          invoice_data["supplier_gstin"], invoice_data["customer_gstin"], 
          invoice_data["subtotal"], invoice_data["tax"], invoice_data["total"]))
    conn.commit()
    conn.close()

invoice_data = {
    "invoice_number": invoice_number,
    "invoice_date": invoice_date,
    "supplier": supplier,
    "customer": customer,
    "billing_address": billing_address,
    "shipping_address": shipping_address,
    "supplier_gstin": supplier_gstin,
    "customer_gstin": customer_gstin,
    "subtotal": subtotal,
    "tax": tax,
    "total": total
}

save_invoice_to_db(invoice_data)
print("Invoice saved to database successfully!")
