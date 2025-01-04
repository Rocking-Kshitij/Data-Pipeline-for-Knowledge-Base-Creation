import psycopg2
import csv, os, time

def find_csv_files(folder_path):
    """
    Searches a folder for files ending with .csv and returns their names.

    Args:
        folder_path (str): Path to the folder to search.

    Returns:
        list: List of .csv file names in the folder.
    """
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        
        # Filter files ending with .csv
        csv_files = [file for file in files if file.endswith('.csv')]
        
        return csv_files
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []


def save_to_db(file_path):
    print("Saving data to PostgreSQL...")
    conn = psycopg2.connect(
        dbname="pipeline_db",
        user="data_postgreuser",
        password="data_postgre_password",
        host="localhost",
        port='5431',
    )
    cursor = conn.cursor()

    # Example: Save movies data
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            cursor.execute(
                """
                INSERT INTO movies (MovieID, Title, Genres, Rating, Year) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (MovieID) DO NOTHING
                """,
                row[:5],  # Adjust based on your schema
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("Data saved to PostgreSQL.")

def run():
    print("I am saving data sql function", flush = True)
    file_name = find_csv_files("../data/processed/cleaned_movies.csv")[0]
    save_to_db(f"../data/processed/cleaned_movies.csv/{file_name}")
