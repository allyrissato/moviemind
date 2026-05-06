import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p"
TIMEOUT = 10


def has_api_key() -> bool:
    return bool(API_KEY and API_KEY != "sua_chave_aqui")


@lru_cache(maxsize=512)
def search_movie(movie_name: str) -> dict | None:
    """Busca um filme no TMDB. Se não tiver chave, retorna None sem quebrar o app."""
    if not has_api_key():
        return None

    try:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={"api_key": API_KEY, "query": movie_name, "language": "pt-BR"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        return results[0] if results else None
    except requests.RequestException:
        return None


def fetch_movie_poster(movie_name: str) -> str | None:
    movie = search_movie(movie_name)
    if not movie:
        return None

    poster_path = movie.get("poster_path")
    if poster_path:
        return f"{IMAGE_BASE}/w500{poster_path}"
    return None


def fetch_movie_details(movie_name: str) -> dict | None:
    movie = search_movie(movie_name)
    if not movie:
        return None

    backdrop_path = movie.get("backdrop_path")
    poster_path = movie.get("poster_path")

    return {
        "title": movie.get("title") or movie_name,
        "overview": movie.get("overview") or "Descrição não disponível.",
        "rating": round(movie.get("vote_average") or 0, 1),
        "year": (movie.get("release_date") or "")[:4] or "Não informado",
        "backdrop": f"{IMAGE_BASE}/original{backdrop_path}" if backdrop_path else None,
        "poster": f"{IMAGE_BASE}/w500{poster_path}" if poster_path else None,
    }
