import re

# Validate unstructured data
def validate_articles(file_path):
    print("Validating unstructured data...")
    with open(file_path, "r") as file:
        lines = file.readlines()

    token_lengths = []
    embedding_counts = []
    for line in lines:
        text, embedding = line.split("\t")
        tokens = text.split()
        token_lengths.append(len(tokens))
        embedding_counts.append(len(eval(embedding)))  # Convert string back to list

    # Check if token lengths and embedding lengths are consistent
    print(f"Minimum token length: {min(token_lengths)}, Maximum token length: {max(token_lengths)}")
    print(f"Embedding dimensions: {set(embedding_counts)}")

    if len(set(embedding_counts)) == 1:
        print("Unstructured data validation passed.")
    else:
        print("Unstructured data validation failed. Check embedding dimensions.")

# Path to processed embeddings
embeddings_file_path = "../data/processed/article_embeddings.txt"

def run():
    # Validate the articles data
    validate_articles(embeddings_file_path)
