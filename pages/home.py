import streamlit as st

from api.anilist import (
    get_trending_anime,
    get_popular_anime,
    get_new_releases,
    search_anime,
)

from components.hero import render_hero
from components.anime_grid import render_anime_section


    
def render_home(search):
    trending = get_trending_anime()
    popular = get_popular_anime()
    new_releases = get_new_releases()

    if search.strip():
        with st.spinner("Searching AniList..."):
            results = search_anime(
                search,
                per_page=20,
            )

        if results:
            render_anime_section(
                "Search Results",
                results,
                prefix="search",
            )
        else:
            st.info("No anime found.")

        return

    render_hero(trending)

    render_anime_section(
        "Trending Now",
        trending,
        prefix="trending",
    )

    render_anime_section(
        "Popular Anime",
        popular,
        prefix="popular",
    )

    render_anime_section(
        "New Releases",
        new_releases,
        prefix="new",
    )
    
    
    
    
    
    
    
    
    

