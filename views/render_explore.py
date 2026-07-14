import streamlit as st
from api.anilist import explore_anime
from components.anime_grid import render_anime_section


def render_explore():
    if "explore_page" not in st.session_state:
        st.session_state.explore_page = 1
    st.title("Explore Anime")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        genre = st.selectbox(
            "Genre",
            [
                "All",
                "Action",
                "Adventure",
                "Comedy",
                "Drama",
                "Fantasy",
                "Romance",
                "Sci-Fi",
                "Slice of Life",
                "Sports",
                "Supernatural",
            ],
        )

    with col2:
        year = st.selectbox(
            "Year",
            ["All"] + list(range(2026, 1999, -1)),
        )

    with col3:
        season = st.selectbox(
            "Season",
            [
                "All",
                "WINTER",
                "SPRING",
                "SUMMER",
                "FALL",
            ],
        )

    with col4:
        sort_label = st.selectbox(
            "Sort By",
            [
                "Popularity",
                "Trending",
                "Score",
                "Newest",
            ],
        )
        
        
    current_filters = (
    genre,
    year,
    season,
    sort_label,
)

    if "explore_filters" not in st.session_state:
        st.session_state.explore_filters = current_filters

    elif st.session_state.explore_filters != current_filters:
        st.session_state.explore_page = 1
        st.session_state.explore_filters = current_filters    
        

        
    genre_value = None if genre == "All" else genre
    year_value = None if year == "All" else year
    season_value = None if season == "All" else season

    sort_map = {
        "Popularity": "POPULARITY_DESC",
        "Trending": "TRENDING_DESC",
        "Score": "SCORE_DESC",
        "Newest": "START_DATE_DESC",
    }

    sort_value = sort_map[sort_label]

    with st.spinner("Discovering anime..."):
        anime_results = explore_anime(
            genre=genre_value,
            year=year_value,
            season=season_value,
            sort=sort_value,
            page=st.session_state.explore_page,
            per_page=20,
        )

    if anime_results:
        render_anime_section(
            "Explore Results",
            anime_results,
            prefix="explore",
        )
    else:
        st.info("No anime found for these filters.")
  
    
    st.markdown("---")

    prev_col, page_col, next_col = st.columns(
        [1, 2, 1]
    )

    with prev_col:
        if st.button(
            "← Previous",
            disabled=st.session_state.explore_page <= 1,
            use_container_width=True,
        ):
            st.session_state.explore_page -= 1
            st.rerun()

    with page_col:
        st.markdown(
            f"<div style='text-align:center; padding-top:8px;'>"
            f"Page {st.session_state.explore_page}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with next_col:
        if st.button(
            "Next →",
            disabled=len(anime_results) < 20,
            use_container_width=True,
        ):
            st.session_state.explore_page += 1
            st.rerun()
            


