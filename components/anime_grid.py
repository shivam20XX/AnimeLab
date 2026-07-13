import streamlit as st

from components.anime_card import anime_card


def render_anime_section(title, anime_list, prefix):
    st.subheader(title)

    columns = st.columns(5)

    for index, anime in enumerate(anime_list[:30]):
        with columns[index % 5]:
            anime_card(
                anime,
                key_prefix=prefix,
            )