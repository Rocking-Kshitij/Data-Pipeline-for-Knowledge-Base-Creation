import psycopg2
from sentence_transformers import SentenceTransformer

db_config={
    "dbname": "pipeline_vector_db",
    "user": "data_pgvector_user",
    "password": "data_pgvector_password",
    "host": "localhost",
    "port": "5435"
}


def query_knowledge_base(query, db_config, top_k=5):
    print("Querying the knowledge base...")
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Pre-trained model for embeddings
    query_embedding = model.encode([query])[0]  # Generate query embedding
    comma_seperated_embedding ="'["+ ",".join(map(str, query_embedding))+"]'"
    # print(comma_seperated_embedding, flush =True)
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"],
    )
    cursor = conn.cursor()
    query = f"""
    SELECT topic, article, 1 - (embedding <=> {comma_seperated_embedding}) AS similarity
    FROM article_embeddings ORDER BY similarity DESC
    LIMIT {top_k}
    """
    # print(query, flush= True)
    # Perform similarity search
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

print("Ask your question from RAG db")
query = input("Enter here: ")
result = query_knowledge_base(query, db_config)
print("Gathering results")
for idx, (topic, article, similarity) in enumerate(result, 1):
    print(f"{idx}. Article: {article[:100]}... (Similarity: {similarity:.4f})")
print("\n",result[0][0],": ", result[0][1])

