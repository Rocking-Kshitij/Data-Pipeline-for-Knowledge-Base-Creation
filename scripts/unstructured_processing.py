import os
import re
import psycopg2
from sentence_transformers import SentenceTransformer

db_config={
    "dbname": "pipeline_vector_db",
    "user": "data_pgvector_user",
    "password": "data_pgvector_password",
    "host": "localhost",
    "port": "5435"
}
# Preprocessing: Remove stop words and tokenize
def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r"[^\w\s]", "", text.lower())
    # Tokenize words
    tokens = text.split()
    # Remove stop words (basic example)
    stop_words = {"abuse", "abusing language"}
    return " ".join([word for word in tokens if word not in stop_words])

def split_topic(articles):
    topics = list()
    art = list()
    for idx, item in enumerate(articles):
        if item[0:7] == "Article" and articles[idx+1] !="Article":
            topics.append(item[item.find(item.split(" ")[2]):-1])
            art.append(articles[idx+1])
    return topics, art


# Generate embeddings
def generate_embeddings(articles):
    print("Processing unstructured data...")
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Pre-trained model for embeddings
    topics, articles = split_topic(articles)
    processed_articles = [preprocess_text(article) for article in articles]
    print(topics, flush=True)
    print(processed_articles, flush=True)
    embeddings = model.encode(processed_articles)
    return topics, processed_articles, embeddings

    # # Save embeddings and processed text
    # os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # with open(output_path, "w") as file:
    #     for article, embedding in zip(processed_articles, embeddings):
    #         file.write(f"{article}\t{embedding.tolist()}\n")
    # print(f"Unstructured data processing completed. Embeddings saved to {output_path}")

def store_embeddings(topics, processed_articles, embeddings):
    print("I  am now preparing to store embeddings", flush=True)
    conn = psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"],
    )
    cursor = conn.cursor()

        # Insert embeddings into the database
    for topic, article, embedding in zip(topics, processed_articles, embeddings):
        cursor.execute(
            """
            INSERT INTO article_embeddings (topic, article, embedding)
            VALUES (%s, %s, %s)
            """,
            (topic, article, embedding.tolist()),
        )
    conn.commit()
    cursor.close()
    conn.close()
    print("Embeddings saved to PostgreSQL.")


# Paths to raw and processed data
articles_input_path = "../data/raw/articles.txt"
embeddings_output_path = "../data/processed/article_embeddings.txt"

def run():
    # Load articles and process
    with open(articles_input_path, "r") as file:
        articles = file.readlines()
    topics, processed_articles, embeddings = generate_embeddings(articles)
    print("Embedding size:", len(embeddings[0]))
    store_embeddings(topics, processed_articles, embeddings)