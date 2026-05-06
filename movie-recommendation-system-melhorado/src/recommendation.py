import re
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = Path("data/movies.csv")


def load_movies(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Carrega e prepara a base de filmes."""
    movies = pd.read_csv(path)
    movies["genres"] = movies["genres"].fillna("Unknown")
    movies["clean_title"] = movies["title"].apply(clean_title)
    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)")[0].fillna("Não informado")
    movies["genres_text"] = movies["genres"].str.replace("|", " ", regex=False)
    movies["content"] = movies["clean_title"] + " " + movies["genres_text"]
    return movies


def clean_title(title: str) -> str:
    """Remove o ano do título para facilitar busca na API TMDB."""
    return re.sub(r"\s*\(\d{4}\)", "", str(title)).strip()


def build_similarity(movies: pd.DataFrame):
    """Cria a matriz de similaridade a partir do título e gêneros."""
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(movies["content"])
    similarity = cosine_similarity(matrix, matrix)
    indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()
    return similarity, indices


def recommend(movie_title: str, movies: pd.DataFrame, similarity, indices, num_recommendations: int = 8) -> pd.DataFrame:
    """Retorna um DataFrame com filmes parecidos."""
    if movie_title not in indices:
        return pd.DataFrame()

    idx = indices[movie_title]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
    movie_indices = [i[0] for i in scores]
    return movies.iloc[movie_indices].copy()


def filter_movies(movies: pd.DataFrame, search: str = "", genre: str = "Todos") -> pd.DataFrame:
    """Filtra filmes por texto e gênero."""
    result = movies.copy()

    if search:
        search = search.lower().strip()
        result = result[
            result["title"].str.lower().str.contains(search, na=False)
            | result["clean_title"].str.lower().str.contains(search, na=False)
            | result["genres"].str.lower().str.contains(search, na=False)
        ]

    if genre != "Todos":
        result = result[result["genres"].str.contains(genre, case=False, na=False)]

    return result


def get_all_genres(movies: pd.DataFrame) -> list[str]:
    genres = set()
    for value in movies["genres"].dropna():
        for genre in str(value).split("|"):
            if genre and genre != "(no genres listed)":
                genres.add(genre)
    return sorted(genres)
