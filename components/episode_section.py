import html
from textwrap import dedent

import streamlit as st

from api.yt import (
    search_youtube,
    group_videos_by_season,
    MUSE_INDIA_CHANNEL_ID,
)


def render_episode_section(anime, anime_title):
    st.markdown("## Watch Episodes")

    videos = search_youtube(
        anime_title,
        channel_id=MUSE_INDIA_CHANNEL_ID,
    )

    if not videos:
        st.info(
            "No official YouTube episodes found for this anime."
        )
        return

    seasons = group_videos_by_season(videos)

    if not seasons:
        seasons = {
        1: [
            {
                **video,
                "season_number": 1,
                "season_episode": index + 1,
            }
            for index, video in enumerate(videos)
        ]
    }

    season_numbers = sorted(seasons.keys())

    selected_season = st.selectbox(
        "Season",
        options=season_numbers,
        format_func=lambda season: f"Season {season}",
        key=f"season_selector_{anime['id']}",
    )

    season_videos = seasons[selected_season]

    st.caption(
        f"{len(season_videos)} episodes found on YouTube"
    )

    selected_video_id = st.query_params.get("video")

    if selected_video_id:
        st.markdown("### Now Playing")

        st.video(
            f"https://www.youtube.com/watch?v={selected_video_id}"
        )

    columns = st.columns(4)

    for index, video in enumerate(season_videos):
        with columns[index % 4]:
            episode_number = video["season_episode"]

            episode_html = (
            f'<a class="episode-card-link" '
            f'href="?anime={anime["id"]}&video={video["video_id"]}" '
            f'target="_self">'
            f'<div class="episode-card">'
            f'<div class="episode-thumbnail-wrap">'
            f'<img class="episode-thumbnail" '
            f'src="{html.escape(video["thumbnail"], quote=True)}" '
            f'alt="Episode {episode_number}">'
            f'<div class="episode-play-overlay">'
            f'<div class="episode-play-icon">▶</div>'
            f'</div></div>'
            f'<div class="episode-card-body">'
            f'<div class="episode-number">Episode {episode_number}</div>'
            f'<div class="episode-title">{html.escape(video["title"])}</div>'
            f'</div></div></a>'
            )
            
            st.markdown(
                episode_html,
                unsafe_allow_html=True,
            )