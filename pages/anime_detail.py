import html
import streamlit as st
import re

from components.anime_card import get_title
from components.cast_section import render_cast_sections
from components.episode_section import render_episode_section
from utils.text import clean_description
from utils.text import clean_description




#? ----- Porvides details of the selected anime when clicked on the card -----
def render_anime_detail(anime):
    title = get_title(anime)

    safe_title = html.escape(title)

    description = clean_description(
        anime.get("description")
        or "No description available."
    )

    banner = (
        anime.get("bannerImage")
        or anime["coverImage"]["extraLarge"]
    )

    cover = anime["coverImage"]["extraLarge"]

    genres = anime.get("genres") or []

    studios = [
        studio["name"]
        for studio in anime.get("studios", {}).get("nodes", [])
    ]

#?-------- Banner ---------------

    detail_banner_html = (
        f'<div class="detail-banner" '
        f'style="background-image:'
        f'linear-gradient(to top, #05070c 0%, transparent 75%),'
        f'url(\'{banner}\');">'
        f'</div>'
    )

    st.markdown(
        detail_banner_html,
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1, 3],
        gap="large",
    )

    with left:
        st.image(
            cover,
            use_container_width=True,
        )

    with right:
        st.markdown(
            f'<div class="detail-title">'
            f'{safe_title}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.write(description)

        studios_text = ", ".join(studios) or "Unknown"
        genres_text = " • ".join(genres) or "Unknown"

        info_html = (
            f'<div class="detail-info-card">'
            f'<div class="detail-info-grid">'
            f'<div class="detail-info-item">'
            f'<span class="info-label">⭐ Score</span>'
            f'<span class="info-value">{anime.get("averageScore") or "N/A"}</span>'
            f'</div>'
            f'<div class="detail-info-item">'
            f'<span class="info-label">🎬 Episodes</span>'
            f'<span class="info-value">{anime.get("episodes") or "Ongoing"}</span>'
            f'</div>'
            f'<div class="detail-info-item">'
            f'<span class="info-label">⏱ Duration</span>'
            f'<span class="info-value">{anime.get("duration") or "Unknown"} min</span>'
            f'</div>'
            f'<div class="detail-info-item">'
            f'<span class="info-label">📅 Year</span>'
            f'<span class="info-value">{anime.get("seasonYear") or "Unknown"}</span>'
            f'</div>'
            f'<div class="detail-info-item">'
            f'<span class="info-label">📺 Status</span>'
            f'<span class="info-value">{anime.get("status") or "Unknown"}</span>'
            f'</div>'
            f'<div class="detail-info-item">'
            f'<span class="info-label">🏢 Studio</span>'
            f'<span class="info-value">{html.escape(studios_text)}</span>'
            f'</div>'
            f'</div>'
            f'<div class="detail-genres">'
            f'<span class="info-label">Genres</span>'
            f'<span class="genre-text">{html.escape(genres_text)}</span>'
            f'</div>'
            f'</div>'
        )

        st.markdown(info_html, unsafe_allow_html=True)

        # if genres:
        #     st.markdown(
        #         "**Genres:** "
        #         + " • ".join(genres)
        #     )



    characters = anime.get("characters", {}).get("edges", [])

    # -------------------------
    #? Characters & voice cast
    # -------------------------

    render_cast_sections(anime)

#?---- episode number extractor ----     
    render_episode_section(
    anime,
    get_title(anime),
)

