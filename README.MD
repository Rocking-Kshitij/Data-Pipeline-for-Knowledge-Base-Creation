# Data Pipeline for Knowledge Base Creation

## **Project Overview**
This project is a data pipeline designed for creating a knowledge base for Retrieval-Augmented Generation (RAG) systems. It processes both structured and unstructured data, generates embeddings for the text, and stores them in a vector database to enable efficient similarity searches.

### **Key Features**
1. **Data Ingestion**:
   - Processes structured data (e.g., `movies.csv`).
   - Parses unstructured text data (e.g., `articles.txt`).
2. **Data Processing**:
   - Cleans and normalizes structured data using PySpark.
   - Preprocesses unstructured text and generates embeddings using `SentenceTransformer`.
3. **Data Quality Validation**:
   - Validates data completeness and schema consistency.
4. **Orchestration**:
   - Uses Apache Airflow to automate and orchestrate the pipeline tasks.
5. **Knowledge Base**:
   - Stores embeddings in a PostgreSQL vector database (using `pgvector`).
   - Provides a query interface for similarity search.

---

## **Directory Structure**
```plaintext
Data Pipeline for Knowledge Base Creation/
├── airflow/
│   ├── config/
│   ├── dags/
│   │   └── data_pipeline_dag.py
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yml
├── data/
│   ├── processed/
│   ├── raw/
│   │   ├── movies.csv
│   │   └── articles.txt
├── scripts/
│   ├── api_server.py
│   ├── data_ingestion.py
│   ├── save_to_postgresql.py
│   ├── structured_processing.py
│   ├── structured_validation.py
│   ├── unstructured_processing.py
│   └── unstructured_validation.py
├── env/
├── requirements.txt
└── README.md
```

---

## **Setup Instructions**

### **1. Prerequisites**
- Docker
- Python 3.8+
- PostgreSQL with `pgvector` extension

### **2. Environment Setup**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Data Pipeline for Knowledge Base Creation
   ```
2. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Docker containers for Airflow and PostgreSQL:
   ```bash
   cd airflow
   docker-compose up -d
   ```
5. Initialize Airflow:
   ```bash
   docker exec -it airflow-webserver airflow db init
   docker exec -it airflow-webserver airflow users create \  
      --username admin \  
      --password admin \  
      --firstname Admin \  
      --lastname User \  
      --role Admin \  
      --email admin@example.com
   ```
6. Install `pgvector` extension on PostgreSQL:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

---

## **Pipeline Phases**

### **Phase 1: Environment Setup**
- Installed dependencies and configured project environment.
- Set up Airflow, PostgreSQL, and directory structure.

### **Phase 2: Data Pipeline Implementation**
1. **Data Ingestion**:
   - Loaded structured and unstructured data.
   - Created Python scripts for ingestion.
2. **Data Processing**:
   - Cleaned structured data using PySpark.
   - Preprocessed unstructured text and generated embeddings using `SentenceTransformer`.
3. **Data Quality Validation**:
   - Validated completeness and schema consistency of the data.

### **Phase 3: Orchestration**
- Created Airflow DAG to automate pipeline tasks:
  - Data ingestion
  - Data processing (structured and unstructured)
  - Validation
  - Saving processed data to PostgreSQL

### **Phase 4: Knowledge Base and Query Interface**
1. **Searchable Knowledge Base**:
   - Stored embeddings in PostgreSQL vector database.
   - Implemented a similarity search using cosine similarity.
2. **Query Interface**:
   - Built a Python script to accept user queries and retrieve relevant documents from the database.

---

## **Usage Instructions**

### **1. Running the Pipeline**
1. Start the FastAPI server:
   ```bash
   python scripts/api_server.py
   ```
2. Access the Airflow portal at `http://localhost:8080`.
3. Trigger the `data_pipeline` DAG to run all pipeline phases.

### **2. Query the Knowledge Base**
1. Run the query interface:
   ```bash
   python scripts/query_interface.py
   ```
2. Enter a query when prompted, e.g.,
   ```plaintext
   Enter here: What is machine learning?
   ```
3. View the most relevant articles and similarity scores.

---

## **Future Enhancements**
1. Scale to larger datasets with distributed databases.
2. Add support for additional vector databases like Pinecone or Weaviate.
3. Integrate with a web interface for querying the knowledge base.
4. Implement advanced preprocessing techniques for improved embeddings.

---

## **Acknowledgments**
- Libraries: `SentenceTransformer`, `pgvector`, `FastAPI`, `PySpark`
- Tools: Apache Airflow, PostgreSQL

---

## **Contact**
For any queries or suggestions, please reach out to [your email/contact info].
