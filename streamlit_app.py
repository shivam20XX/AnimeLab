import streamlit as st
import html ,re
from api.yt import (
    search_youtube,
    extract_episode_number,
    group_videos_by_season,
    MUSE_INDIA_CHANNEL_ID,
)


from api.anilist import (
    get_trending_anime,
    get_popular_anime,
    get_new_releases,
    get_anime_details,
)
from components.anime_card import anime_card, get_title


st.set_page_config(
    page_title="AniLab",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

def clean_description(text):
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text)



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
    # Characters
    # -------------------------

    if characters:
        st.markdown("## Characters")

        character_columns = st.columns(8)

        for index, edge in enumerate(characters[:8]):
            character = edge["node"]

            with character_columns[index]:
                st.image(
                    character["image"]["large"],
                    use_container_width=True,
                )

                st.markdown(
                    f"**{character['name']['full']}**"
                )

                st.caption(
                    edge.get("role", "Unknown")
                )

    # -------------------------
    # Voice Cast
    # -------------------------

    cast_items = []
    seen_actor_ids = set()

    for edge in characters:
        voice_actors = edge.get("voiceActors") or []

        for voice_actor in voice_actors:
            actor_id = voice_actor.get("id")

            if actor_id is None:
                continue

            if actor_id in seen_actor_ids:
                continue

            seen_actor_ids.add(actor_id)

            cast_items.append({
                "image": (
                    voice_actor.get("image", {}).get("large")
                ),
                "actor_name": (
                    voice_actor.get("name", {}).get("full")
                    or "Unknown"
                ),
                "character_name": (
                    edge.get("node", {})
                    .get("name", {})
                    .get("full")
                    or "Unknown"
                ),
            })

            if len(cast_items) >= 8:
                break

        if len(cast_items) >= 8:
            break

    if cast_items:
        st.markdown("## Voice Cast")

        cast_columns = st.columns(len(cast_items))

        for index, cast in enumerate(cast_items):
            with cast_columns[index]:

                if cast["image"]:
                    st.image(
                        cast["image"],
                        use_container_width=True,
                    )

                st.markdown(
                    f"**{cast['actor_name']}**"
                )

                st.caption(
                    f"as {cast['character_name']}"
                )
    else:
        st.caption("Voice cast information unavailable.")
        


#?---- episode number extractor ----     
    st.markdown("## Watch Episodes")

    anime_title = get_title(anime)

    videos = search_youtube(
        anime_title,
    channel_id=MUSE_INDIA_CHANNEL_ID,
)

    if videos:
        seasons = group_videos_by_season(videos)

    if seasons:
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

        playing_key = f"playing_video_{anime['id']}"

        if playing_key not in st.session_state:
            st.session_state[playing_key] = None

        # Player
        if st.session_state[playing_key]:
            st.video(
                "https://www.youtube.com/watch?v="
                + st.session_state[playing_key]
            )

        # Episode cards
        columns = st.columns(4)

        for index, video in enumerate(season_videos):
            with columns[index % 4]:

                st.image(
                    video["thumbnail"],
                    use_container_width=True,
                )

                episode_number = video["season_episode"]

                st.markdown(
                    f"**Episode {episode_number}**"
                )

                st.caption(video["title"])

                if st.button(
                    "▶ Play",
                    key=f"play_{anime['id']}_{video['video_id']}",
                    use_container_width=True,
                ):
                    st.session_state[playing_key] = (
                        video["video_id"]
                    )
                    st.rerun()

        else:
                st.info(
            "Videos were found, but season information "
            "could not be detected."
        )
    else:
      st.info(
        "No official YouTube episodes found for this anime."
    )



st.markdown(
    
    """
    <style>
    .anime-poster-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 2 / 3;
    overflow: hidden;
    border-radius: 14px;
    background: #11141c;
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.25s ease, border-color 0.25s ease;
}

.anime-poster {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
}

.anime-card-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 14px;
    box-sizing: border-box;
    background: linear-gradient(
        to top,
        rgba(5,7,12,0.98) 0%,
        rgba(5,7,12,0.65) 25%,
        transparent 60%
    );
}

.anime-card-title {
    color: white;
    font-size: 15px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 7px;
}

.anime-card-meta {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #d1d5db;
    font-size: 12px;
}

.anime-poster-wrap:hover {
    transform: translateY(-5px);
    border-color: #a855f7;
}

.anime-poster-wrap:hover .anime-poster {
    transform: scale(1.06);
}
    
    .anime-card-link {
    display: block;
    text-decoration: none !important;
    color: inherit !important;
    cursor: pointer;
}

.anime-card-link:hover {
    text-decoration: none !important;
}
    
    
    
    
    .stApp {
        background:
            radial-gradient(
                circle at 70% 0%,
                #19102e 0%,
                #090b12 32%,
                #05070c 70%
            );
    }

    [data-testid="stSidebar"] {
        background: #080b12;
        border-right: 1px solid #1c2230;
    }

    [data-testid="stSidebar"] h1 {
        color: #a855f7;
    }

    .block-container {
        padding-top: 4rem;
        padding-bottom: 5rem;
    }

    .hero {
        min-height: 390px;

        padding:
            70px
            50px;

        border-radius: 20px;

        background-size: cover;
        background-position: center;

        display: flex;
        align-items: flex-end;

        margin-bottom: 35px;

        box-shadow:
            0 25px 80px
            rgba(0, 0, 0, 0.5);
    }

    .hero-content {
        max-width: 620px;
    }

    .hero-badge {
        display: inline-block;

        background: #7c3aed;

        padding: 6px 12px;

        border-radius: 999px;

        font-size: 12px;
        font-weight: 700;

        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;

        line-height: 1;

        margin-bottom: 15px;
    }

    .hero-meta {
        color: #d4d4d8;
        margin-bottom: 15px;
    }

    .hero-description {
        color: #c4c4cc;
        font-size: 15px;
        line-height: 1.6;
    }

    .anime-title {
        font-weight: 700;

        font-size: 15px;

        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;

        margin-top: 7px;
    }

    .anime-meta {
        color: #9ca3af;

        font-size: 13px;

        margin-top: 4px;
        margin-bottom: 8px;
    }

    [data-testid="stImage"] img {
        border-radius: 12px;
    }
    
    .detail-banner {
    width: 100%;
    height: 380px;
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    margin-top: 20px;
    margin-bottom: -100px;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.55);
}

.detail-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.05;
    margin-top: 110px;
    margin-bottom: 25px;
}

.detail-info-card {
    padding: 20px;
    margin: 20px 0;

    background: rgba(17, 20, 28, 0.82);

    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;

    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.25);
}

##--- Anime Details Section ---##

.detail-info-card {
    padding: 22px 26px;
    margin: 20px 0;
    background: rgba(17, 20, 28, 0.88);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
}

.detail-info-grid {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    column-gap: 40px;
    row-gap: 22px;
    width: 100%;
}

.detail-info-item {
    display: flex !important;
    flex-direction: column;
    gap: 6px;
    min-width: 0;
}

.info-label {
    display: block;
    color: #9ca3af;
    font-size: 13px;
    font-weight: 600;
}

.info-value {
    display: block;
    color: white;
    font-size: 17px;
    font-weight: 700;
}

.detail-genres {
    margin-top: 24px;
    padding-top: 18px;
    border-top: 1px solid rgba(255,255,255,0.08);
}

.genre-text {
    display: block;
    margin-top: 8px;
    color: #d8b4fe;
    font-size: 15px;
}

@media (max-width: 800px) {
    .detail-info-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600)
def load_homepage_data():
    return {
        "trending": get_trending_anime(25),
        "popular": get_popular_anime(50),
        "new": get_new_releases(30),
    }


data = load_homepage_data()

trending = data["trending"]
popular = data["popular"]
new_releases = data["new"]



selected_anime_id = st.query_params.get("anime")

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


    for video in videos:
     st.write(
        video["title"],
        "—",
        video["channel"],
        "—",
        video["channel_id"],
    )




# --------------------
# Sidebar
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


# --------------------
# Header
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
# Search Results
# --------------------

if search:

    search_lower = search.lower()

    results = [

        anime

        for anime in trending + popular + new_releases

        if search_lower in get_title(anime).lower()

    ]

    unique_results = {
        anime["id"]: anime
        for anime in results
    }.values()

    st.subheader("Search Results")

    columns = st.columns(5)

    for index, anime in enumerate(unique_results):

        with columns[index % 5]:

            anime_card(
                anime,
                key_prefix="search",
            )

    st.stop()


# --------------------
# Hero
# --------------------

hero = trending[3]

hero_title = get_title(hero)

hero_banner = (
    hero.get("bannerImage")
    or hero["coverImage"]["extraLarge"]
)

hero_description = clean_description(
    hero.get("description")
    or "Discover trending anime on AniTube."
)

hero_description = hero_description[:260]
hero_html = f"""
<div class="hero" style="background-image:
linear-gradient(
    90deg,
    rgba(5,7,12,0.98) 0%,
    rgba(5,7,12,0.78) 40%,
    rgba(5,7,12,0.20) 100%
),
url('{hero_banner}');">

<div class="hero-content">

<div class="hero-badge">Trending</div>

<div class="hero-title">
{html.escape(hero_title)}
</div>

<div class="hero-meta">
⭐ {hero.get("averageScore") or "N/A"}
&nbsp; • &nbsp;
{hero.get("seasonYear") or "Unknown"}
&nbsp; • &nbsp;
{html.escape(", ".join(hero.get("genres", [])[:3]))}
</div>

<div class="hero-description">
{html.escape(hero_description)}
</div>

</div>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# --------------------
# Reusable Section
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
# Homepage Sections
# --------------------

anime_section(
    "🔥 Trending Now",
    trending,
    "trending",
)

anime_section(
    "⭐ Popular Anime",
    popular,
    "popular",
)

anime_section(
    "🆕 New Releases",
    new_releases,
    "new",
)


