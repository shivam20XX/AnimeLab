import streamlit as st
from pathlib import Path
from components.hero import render_hero
from components.anime_grid import render_anime_section
from views.home import render_home
from views.render_explore import render_explore

from api.anilist import (
    get_trending_anime,
    get_popular_anime,
    get_new_releases,
    get_anime_details,
    search_anime,
)
from components.anime_card import anime_card, get_title
from views.anime_detail import render_anime_detail


##?----- CSS Loader -----
def load_css(file_path):
    css = Path(file_path).read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="AniLab",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
load_css("styles/main.css")


# @st.cache_data(ttl=3600)
# def load_homepage_data():
#     return {
#         "trending": get_trending_anime(25),
#         "popular": get_popular_anime(50),
#         "new": get_new_releases(30),
#     }

# data = load_homepage_data()

# trending = data["trending"]
# popular = data["popular"]
# new_releases = data["new"]

selected_anime_id = st.query_params.get("anime")

if selected_anime_id:
    try:
        selected_anime_id = int(selected_anime_id)
    except ValueError:
        st.error("Invalid anime ID.")
        st.stop()

    selected_anime = get_anime_details(selected_anime_id)
    render_anime_detail(selected_anime)
    st.stop()

    # for video in videos:
    #  st.write(
    #     video["title"],
    #     "—",
    #     video["channel"],
    #     "—",
    #     video["channel_id"],
    # )
     

# --------------------
#? Sidebar
# --------------------

with st.sidebar:

    st.title("▶ AniLab")

    st.caption(
        "Anime discovery & official YouTube releases"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Explore",
            "Trending",
            "New Releases",
            "Watchlist",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.caption("Powered by AniList")



if page == "Explore":
    render_explore()
    st.stop()



# --------------------
#?------------ Header
# --------------------

header_left, header_right = st.columns(
    [4, 1]
)

with header_left:

    search = st.text_input(
        "Search",
        placeholder="Search anime, genres...",
        label_visibility="collapsed",
    )

with header_right:

    st.button(
        "My Watchlist",
        use_container_width=True,
    )


# --------------------
#? Reusable Section
# --------------------

def anime_section(title, anime_list, prefix):
    st.subheader(title)

    columns = st.columns(5)

    for index, anime in enumerate(anime_list[:10]):
        with columns[index % 5]:
            anime_card(
                anime,
                key_prefix=prefix,
            )


selected_anime_id = st.query_params.get("anime")

if selected_anime_id:
    selected_anime_id = int(selected_anime_id)

    st.write("Selected AniList ID:", selected_anime_id)

# --------------------
#?----- Search Results
# --------------------
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

    st.stop()
    
render_home(search)   