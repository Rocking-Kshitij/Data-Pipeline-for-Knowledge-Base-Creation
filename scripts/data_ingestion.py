import pandas as pd


# Structured Data: Movies
def load_movies(file_path):
    print("Loading structured data...")
    movies_df = pd.read_csv(file_path)
    print("Movies data loaded successfully.")
    return movies_df

# Unstructured Data: Articles
def load_articles(file_path):
    print("Loading unstructured data...")
    with open(file_path, 'r') as file:
        articles = file.readlines()
    print("Articles data loaded successfully.")
    return articles

# Paths to raw data
movies_path = "../data/raw/movies.csv"
articles_path = "../data/raw/articles.txt"


def run():
    # Load Data
    movies_data = load_movies(movies_path)
    articles_data = load_articles(articles_path)

    # Display samples
    print(movies_data.head())
    print("\nSample article:", articles_data[0])
