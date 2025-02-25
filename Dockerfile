# Use Ubuntu as base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=invoice_processor.py
ENV FLASK_RUN_HOST=0.0.0.0

# Initialize the database inside the container
RUN python3 -c "\
import sqlite3; \
conn = sqlite3.connect('/app/invoices.db'); \
cursor = conn.cursor(); \
cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (\
    id INTEGER PRIMARY KEY AUTOINCREMENT, \
    invoice_number TEXT, \
    invoice_date TEXT, \
    supplier TEXT, \
    customer TEXT, \
    billing_address TEXT, \
    shipping_address TEXT, \
    supplier_gstin TEXT, \
    customer_gstin TEXT, \
    subtotal TEXT, \
    tax TEXT, \
    total TEXT\
);'''); \
conn.commit(); \
conn.close();"

# Command to run the application
CMD ["python3", "invoice_processor.py"]

