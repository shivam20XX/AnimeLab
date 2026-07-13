import html
import streamlit as st

from components.anime_card import get_title
from utils.text import clean_description


def render_hero(trending):
    if not trending:
        return

    hero = trending[1]

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