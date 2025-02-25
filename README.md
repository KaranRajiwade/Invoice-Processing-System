# Invoice Processing System with Docker

## 📌 Overview
This project automates invoice processing using Python and Flask. It extracts invoice details from PDFs, fetches supplier information using OpenAI, stores data in SQLite, and provides a REST API to access the data. The application is containerized using Docker for easy deployment.

## 📌 Features
✅ Extract invoice details from emails and PDFs
✅ Fetch supplier details using AI
✅ Store invoices in an SQLite database
✅ REST API to retrieve invoices
✅ Containerized using Docker
✅ Error handling and logging

## **1️⃣ Project Folder Structure**
Ensure your project directory has the following structure before building the Docker image:

```
invoice_processor_project/
│
├── Dockerfile                    # Docker instructions
├── invoice_processor.py           # Main Python script
├── requirements.txt               # Dependencies file
├── invoice_email.eml              # Sample email with invoice
├── invoice.pdf                    # Sample invoice file
├── .env                            # Environment variables (OpenAI API Key)
├── README.md                       # General project documentation
└── invoices.db                     # SQLite database (created inside container)
```

---

## **2️⃣ Setup Instructions (Without Docker)**

### Install Dependencies
If running without Docker, install dependencies manually:
```sh
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the project directory and add:
```
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=sqlite:///invoices.db
```
#### 🔹 Where to Find the OpenAI API Key?
1. Go to [OpenAI's API Page](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Generate a new secret key and replace `your-api-key-here` in the `.env` file

### Initialize the Database
Before running the main script, initialize the database:
```sh
python invoice_processor.py
```
This will create `invoices.db` and set up the required table.

### Run the Program (Without Docker)
To process invoices and start the API, run:
```sh
python invoice_processor.py
```

---

## **3️⃣ Building the Docker Image**
Run the following command inside the **project directory**:
```sh
docker build -t invoice-processor .
```
✅ **Expected Output**:
```
Successfully built <IMAGE_ID>
Successfully tagged invoice-processor:latest
```

---

## **4️⃣ Running the Docker Container**
Start the container and expose the Flask API on port 5000:
```sh
docker run -p 5000:5000 invoice-processor
```
✅ **Expected Output:**
- The Flask API should start and print logs like:
  ```
  * Running on http://0.0.0.0:5000
  ```

---

## **5️⃣ Accessing the API**
Once the container is running, test the API using **cURL** or **Postman**.

🔹 **Check if the API is running**:
```sh
curl http://127.0.0.1:5000/invoices
```
or
📌 Open [http://127.0.0.1:5000/invoices](http://127.0.0.1:5000/invoices) in your browser.

✅ **Expected Output:**
```json
[]
```
(If the database is empty, an empty list will be returned.)

---

## **6️⃣ Checking the Database (Inside the Container)**
To verify that invoices are stored correctly in SQLite:

1️⃣ **Find the running container ID:**
```sh
docker ps
```

2️⃣ **Access the container’s shell:**
```sh
docker exec -it <CONTAINER_ID> bash
```
_(Replace `<CONTAINER_ID>` with the actual container ID)_

3️⃣ **Check stored invoices in SQLite:**
```sh
sqlite3 /app/invoices.db
```
Then, run:
```sql
SELECT * FROM invoices;
```

✅ **Expected Output:**
A list of stored invoices should be displayed.

---

## **7️⃣ Stopping and Removing the Container**
When finished, stop the running container:
```sh
docker ps   # Get the running container ID
docker stop <CONTAINER_ID>
```
To remove the container:
```sh
docker rm <CONTAINER_ID>
```

---

## **8️⃣ Optional: Running in Detached Mode**
To run the container in the background:
```sh
docker run -d -p 5000:5000 invoice-processor
```

---

## **✅ Summary**
1️⃣ **Ensure all project files exist**  
2️⃣ **Install dependencies manually (if not using Docker)**
3️⃣ **Build the image:** `docker build -t invoice-processor .`  
4️⃣ **Run the container:** `docker run -p 5000:5000 invoice-processor`  
5️⃣ **Test the API at:** `http://127.0.0.1:5000/invoices`  
6️⃣ **Check SQLite data inside the container**  
7️⃣ **Stop and clean up the container when done**  

🚀 **Now your Invoice Processing System runs both with and without Docker!** 🎉

