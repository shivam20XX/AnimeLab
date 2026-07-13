import requests,os,re
import streamlit as st
from dotenv import load_dotenv

MUSE_INDIA_CHANNEL_ID = "UCYYhAzgWuxPauRXdPpLAX3Q"

load_dotenv()

YOUTUBE_SEARCH_URL = (
    "https://www.googleapis.com/youtube/v3/search"
)



@st.cache_data(ttl=3600)
def search_youtube(
    query,
    channel_id=None,
    max_pages=2,
):
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY not found.")

    videos = []
    seen_video_ids = set()
    page_token = None

    for _ in range(max_pages):
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 50,
            "order": "relevance",
            "key": api_key,
        }

        if channel_id:
            params["channelId"] = channel_id

        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params=params,
            timeout=15,
        )

        if not response.ok:
            raise RuntimeError(
                f"YouTube API failed: {response.text}"
            )

        payload = response.json()

        for item in payload.get("items", []):
            video_id = item["id"]["videoId"]

            if video_id in seen_video_ids:
                continue

            seen_video_ids.add(video_id)

            videos.append({
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "channel_id": item["snippet"]["channelId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            })

        page_token = payload.get("nextPageToken")

        if not page_token:
            break

    videos.sort(
        key=lambda video: extract_episode_number(
            video["title"]
        )
    )

    return videos
    

def extract_episode_number(title):
    match = re.search(
        r"Episode\s+(\d+)",
        title,
        re.IGNORECASE,
    )

    if match:
        return int(match.group(1))

    return 999999   



def extract_season_episode(title):
    patterns = [
        # (S1E01)
        r"\(S(\d+)E(\d+)\)",

        # S1E01 without brackets
        r"\bS(\d+)E(\d+)\b",

        # Season 1 Episode 01
        r"Season\s*(\d+).*?Episode\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            title,
            re.IGNORECASE,
        )

        if match:
            return (
                int(match.group(1)),
                int(match.group(2)),
            )


    match = re.search(
        r"\bEpisode\s*(\d+)\b",
        title,
        re.IGNORECASE,
    )

    if match:
        return 1, int(match.group(1))

    return None, None


def group_videos_by_season(videos):
    seasons = {}

    for video in videos:
        season, episode = extract_season_episode(
            video.get("title", "")
        )

        if season is None or episode is None:
            continue

        item = video.copy()

        item["season_number"] = season
        item["season_episode"] = episode

        seasons.setdefault(
            season,
            [],
        ).append(item)

    for season_videos in seasons.values():
        season_videos.sort(
            key=lambda video: video["season_episode"]
        )

    return seasons