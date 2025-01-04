-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;


-- Create sample table
CREATE TABLE article_embeddings (
    id SERIAL PRIMARY KEY,
    article TEXT,
    embedding VECTOR(384) -- Adjust dimension if needed
);