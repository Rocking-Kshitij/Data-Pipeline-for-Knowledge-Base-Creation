from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when



# Validate structured data
def validate_movies(spark, file_path):
    print("Validating structured data...")
    movies_df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Check for nulls in critical columns
    null_check = (
        movies_df
        .select(
            [count(when(col(c).isNull(), c)).alias(f"{c}_nulls") for c in ["MovieID", "Title"]]
        )
        .toPandas()
    )
    print("Null values per column:")
    print(null_check)

    # Check for duplicate MovieIDs
    duplicates = movies_df.groupBy("MovieID").count().filter(col("count") > 1).count()
    print(f"Number of duplicate MovieIDs: {duplicates}")

    if null_check.sum(axis=1).values[0] == 0 and duplicates == 0:
        print("Structured data validation passed.")
    else:
        print("Structured data validation failed. Please check the logs.")

# Path to processed movies data
movies_file_path = "../data/processed/cleaned_movies.csv"

def run():
    # Initialize Spark session
    spark = SparkSession.builder.appName("StructuredDataValidation").getOrCreate()
    # Validate the movies data
    validate_movies(spark, movies_file_path)
    spark.stop()