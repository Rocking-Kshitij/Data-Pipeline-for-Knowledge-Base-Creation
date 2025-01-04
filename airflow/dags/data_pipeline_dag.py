import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Function to trigger API calls
def trigger_api(script_name):
    url = f"http://host.docker.internal:8000/run_script/{script_name}"
    response = requests.post(url)
    if response.status_code == 200:
        result = response.json()
        if result["status"] == "success":
            print(f"{script_name} executed successfully.")
        else:
            raise Exception(f"Error: {result['message']}")
    else:
        raise Exception(f"Failed to connect to FastAPI server. Status code: {response.status_code}")

# Default args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
}

# Define the DAG
with DAG(
    "data_pipeline",
    default_args=default_args,
    description="A data pipeline for Knowledge Base creation",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=trigger_api,
        op_args=["data_ingestion"],
    )

    processing_structured_task = PythonOperator(
        task_id="data_processing_structured",
        python_callable=trigger_api,
        op_args=["structured_processing"],
    )
    processing_unstructured_task = PythonOperator(
        task_id="data_processing_unstructured",
        python_callable=trigger_api,
        op_args=["unstructured_processing"],
    )
    validation_structured_task = PythonOperator(
        task_id="data_validation_structured",
        python_callable=trigger_api,
        op_args=["structured_validation"],
    )

    validation_unstructured_task = PythonOperator(
        task_id="data_validation_unstructured",
        python_callable=trigger_api,
        op_args=["unstructured_validation"],
    )

    save_task = PythonOperator(
        task_id="save_to_db",
        python_callable=trigger_api,
        op_args=["save_to_db"],
    )

    ingestion_task >> processing_structured_task >> processing_unstructured_task >> validation_structured_task >> validation_unstructured_task  >> save_task