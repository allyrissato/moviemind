import streamlit as st
import plotly.express as px

from src.recommendation import (
    build_similarity,
    clean_title,
    filter_movies,
    get_all_genres,
    load_movies,
    recommend,
)
from src.tmdb_api import fetch_movie_details, fetch_movie_poster, has_api_key

st.set_page_config(page_title="MovieMind", page_icon="🎬", layout="wide")


@st.cache_data
def get_movies():
    return load_movies()


@st.cache_resource
def get_similarity(_movies):
    return build_similarity(_movies)


movies = get_movies()
cosine_sim, indices = get_similarity(movies)

st.markdown(
    """
<style>
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(255, 79, 216, 0.24), transparent 30%),
        radial-gradient(circle at top right, rgba(0, 212, 255, 0.20), transparent 30%),
        linear-gradient(180deg, #070713 0%, #0c0c1f 45%, #05050c 100%);
    color: white;
}

.hero {
    min-height: 410px;
    border-radius: 30px;
    padding: 42px;
    margin-bottom: 28px;
    display: flex;
    align-items: end;
    background-size: cover;
    background-position: center;
    overflow: hidden;
    position: relative;
    box-shadow: 0 24px 70px rgba(0,0,0,0.55);
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(0,0,0,.92), rgba(0,0,0,.45), rgba(0,0,0,.12));
}

.hero-content {position: relative; z-index: 2; max-width: 850px;}

.logo {
    font-size: 78px;
    line-height: .95;
    font-weight: 1000;
    letter-spacing: 4px;
    margin: 0 0 10px 0;
    background: linear-gradient(90deg, #ff4fd8, #8b5cf6, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 45px rgba(255,79,216,.22);
}

.subtitle {font-size: 19px; color: #e7e7ff; line-height: 1.5;}

.badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff4fd8, #8b5cf6, #00d4ff);
    color: white;
    font-weight: 800;
    margin-bottom: 14px;
}

.movie-card {
    background: rgba(255,255,255,0.065);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 22px;
    padding: 14px;
    min-height: 390px;
    box-shadow: 0 16px 45px rgba(0,0,0,0.32);
    transition: transform .2s ease, border .2s ease;
}

.movie-card:hover {transform: translateY(-6px); border-color: rgba(255,79,216,.65);}

.poster {
    width: 100%;
    height: 285px;
    object-fit: cover;
    border-radius: 18px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #ff4fd8, #8b5cf6, #00d4ff);
}

.movie-title {font-size: 17px; font-weight: 850; margin-bottom: 5px; color: white;}
.movie-meta {font-size: 13px; color: #cfcff7;}
.section-title {font-size: 30px; font-weight: 900; margin: 24px 0 14px 0;}

.metric-card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.10);
    text-align: center;
}

.stButton > button {
    border-radius: 999px;
    border: none;
    background: linear-gradient(90deg, #ff4fd8, #8b5cf6, #00d4ff);
    color: white;
    font-weight: 800;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111124, #070713);
    border-right: 1px solid rgba(255,255,255,.08);
}

@media (max-width: 768px) {
    .logo {font-size: 45px;}
    .hero {min-height: 330px; padding: 25px;}
    .poster {height: 230px;}
}
</style>
""",
    unsafe_allow_html=True,
)


def fallback_background():
    return "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1600&auto=format&fit=crop"


def render_hero(selected_title: str | None = None):
    if selected_title:
        api_title = clean_title(selected_title)
        details = fetch_movie_details(api_title)
    else:
        details = None

    title = details["title"] if details else "MovieMind"
    year = details["year"] if details else "Recomendações inteligentes"
    rating = details["rating"] if details else "IA"
    overview = details["overview"] if details else "Descubra filmes parecidos com os seus favoritos em uma interface inspirada nos maiores serviços de streaming."
    backdrop = details["backdrop"] if details and details.get("backdrop") else fallback_background()

    st.markdown(
        f"""
        <div class="hero" style="background-image: url('{backdrop}');">
            <div class="hero-content">
                <div class="badge">⭐ {rating} • {year}</div>
                <div class="logo">{title}</div>
                <div class="subtitle">{overview}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cards(data, title="Filmes"):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    if data.empty:
        st.warning("Nenhum filme encontrado.")
        return

    cols = st.columns(4)
    for pos, (_, row) in enumerate(data.iterrows()):
        with cols[pos % 4]:
            clean = row.get("clean_title", clean_title(row["title"]))
            poster = fetch_movie_poster(clean)
            if poster is None:
                poster = "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?q=80&w=600&auto=format&fit=crop"

            st.markdown(
                f"""
                <div class="movie-card">
                    <img class="poster" src="{poster}" />
                    <div class="movie-title">{row['title']}</div>
                    <div class="movie-meta">📅 {row['year']}</div>
                    <div class="movie-meta">🎭 {row['genres'].replace('|', ' • ')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def home_page():
    render_hero()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h2>{len(movies)}</h2><p>Filmes na base</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h2>{len(get_all_genres(movies))}</h2><p>Gêneros disponíveis</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h2>TF-IDF</h2><p>Modelo de recomendação</p></div>', unsafe_allow_html=True)

    render_cards(movies.sample(min(8, len(movies)), random_state=42), "🔥 Sugestões em destaque")


def recommendation_page():
    st.markdown("# 🤖 Recomendação inteligente")
    selected_movie = st.selectbox("Escolha um filme que você gosta:", movies["title"].values)
    render_hero(selected_movie)

    if st.button("Me recomendar filmes"):
        recommendations = recommend(selected_movie, movies, cosine_sim, indices, num_recommendations=8)
        render_cards(recommendations, "Filmes recomendados para você")


def catalog_page():
    st.markdown("# 🔎 Catálogo")
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Buscar por título ou gênero")
    with col2:
        genre = st.selectbox("Filtrar por gênero", ["Todos"] + get_all_genres(movies))

    result = filter_movies(movies, search, genre).head(40)
    render_cards(result, "Resultados")


def dashboard_page():
    st.markdown("# 📊 Dashboard")

    genre_rows = []
    for _, row in movies.iterrows():
        for genre in str(row["genres"]).split("|"):
            if genre and genre != "(no genres listed)":
                genre_rows.append({"Gênero": genre})

    col1, col2 = st.columns(2)
    with col1:
        top_genres = (
            __import__("pandas").DataFrame(genre_rows)["Gênero"].value_counts().head(10).reset_index()
        )
        top_genres.columns = ["Gênero", "Quantidade"]
        fig = px.bar(top_genres, x="Gênero", y="Quantidade", title="Top 10 gêneros")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        years = movies[movies["year"] != "Não informado"].copy()
        years["year"] = years["year"].astype(int)
        decade = (years["year"] // 10 * 10).value_counts().sort_index().reset_index()
        decade.columns = ["Década", "Quantidade"]
        fig = px.line(decade, x="Década", y="Quantidade", title="Filmes por década")
        st.plotly_chart(fig, use_container_width=True)


with st.sidebar:
    st.markdown("## 🎬 MovieMind")
    st.caption("Sua próxima experiência cinematográfica começa aqui")

    if not has_api_key():
        st.warning("TMDB_API_KEY não configurada. O app funciona, mas usará imagens reserva.")

    page = st.radio("Navegação", ["Início", "Recomendações", "Catálogo", "Dashboard"])

if page == "Início":
    home_page()
elif page == "Recomendações":
    recommendation_page()
elif page == "Catálogo":
    catalog_page()
elif page == "Dashboard":
    dashboard_page()
