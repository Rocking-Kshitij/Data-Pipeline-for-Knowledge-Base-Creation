from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session


# Load movies.csv into Spark DataFrame
def process_movies(spark, file_path, output_path):
    print("Processing structured data...")
    movies_df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Handle missing values and drop unnecessary columns
    cleaned_df = (
        movies_df
        .dropna(subset=["MovieID", "Title"])  # Remove rows with missing critical data
        .drop(*[col for col in movies_df.columns if "Unnamed" in col])  # Drop extra columns
    )

    # Remove duplicates
    final_df = cleaned_df.dropDuplicates()

    # Save cleaned data to CSV
    final_df.write.csv(output_path, header=True, mode="overwrite")
    print(f"Structured data processing completed. Cleaned data saved to {output_path}")

# Paths to raw and processed data
movies_input_path = "../data/raw/movies.csv"
movies_output_path = "../data/processed/cleaned_movies.csv"

# Process the movies data
def run():
    spark = SparkSession.builder.appName("StructuredDataProcessing").getOrCreate()
    process_movies(spark, movies_input_path, movies_output_path)
    spark.stop()
