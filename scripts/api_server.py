from fastapi import FastAPI
import importlib, os
import structured_processing, structured_validation, unstructured_processing, unstructured_validation, save_to_postgresql, data_ingestion


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.post("/run_script/{script_name}")
def run_script(script_name: str):
    try:
        # Map script names to file paths
        scripts = {
            "data_ingestion": "data_ingestion",
            "structured_processing": "structured_processing",
            "unstructured_processing": "unstructured_processing",
            "structured_validation": "structured_validation",
            "unstructured_validation": "unstructured_validation",
            "save_to_db": "save_to_postgresql",
        }
        if script_name not in scripts:
            return {"status": "error", "message": f"Script {script_name} not found"}
        importlib.import_module(scripts[script_name]).run()
        return {"status": "success", "message": f"Script {script_name} executed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
