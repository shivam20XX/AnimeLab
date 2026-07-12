import html
import streamlit as st


def get_title(anime):
    return (
        anime["title"].get("english")
        or anime["title"].get("romaji")
        or "Unknown"
    )


def anime_card(anime, key_prefix="anime"):
    title = get_title(anime)
    safe_title = html.escape(title)

    image = (
        anime.get("coverImage", {}).get("extraLarge")
        or anime.get("coverImage", {}).get("large")
        or ""
    )

    score = anime.get("averageScore") or "N/A"
    episodes = anime.get("episodes") or "?"

    anime_id = anime["id"]

    card_html = (
        f'<a class="anime-card-link" href="?anime={anime_id}" target="_self">'
        f'<div class="anime-poster-wrap">'
        f'<img class="anime-poster" src="{image}" alt="{safe_title}">'
        f'<div class="anime-card-overlay">'
        f'<div class="anime-card-title">{safe_title}</div>'
        f'<div class="anime-card-meta">'
        f'<span>⭐ {score}</span>'
        f'<span>•</span>'
        f'<span>{episodes} EP</span>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'</a>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )