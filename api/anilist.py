import requests
import streamlit as st

ANILIST_API_URL = "https://graphql.anilist.co"

ANIME_QUERY = """
query ($page: Int, $perPage: Int, $sort: [MediaSort]) {
    Page(page: $page, perPage: $perPage) {
        media(
            type: ANIME
            sort: $sort
            isAdult: false
        ) {
            id
            title {
                english
                romaji
            }
            coverImage {
                extraLarge
                large
            }
            bannerImage
            averageScore
            episodes
            genres
            season
            seasonYear
            status
            description(asHtml: false)
        }
    }
}
"""


ANIME_DETAIL_QUERY = """
query ($id: Int) {
    Media(id: $id, type: ANIME) {
        id

        title {
            english
            romaji
        }

        coverImage {
            extraLarge
            large
        }

        bannerImage
        description(asHtml: false)

        averageScore
        meanScore
        episodes
        duration
        status
        season
        seasonYear
        genres

        studios(isMain: true) {
            nodes {
                name
            }
        }

        characters(
            sort: [ROLE, RELEVANCE, ID]
            perPage: 10
        ) {
            edges {
                role

                node {
                    id
                    name {
                        full
                    }
                    image {
                        large
                    }
                }

                voiceActors(
                    language: JAPANESE
                    sort: [RELEVANCE, ID]
                ) {
                    id
                    name {
                        full
                    }
                    image {
                        large
                    }
                }
            }
        }

        staff(
            sort: [RELEVANCE, ID]
            perPage: 10
        ) {
            edges {
                role

                node {
                    id
                    name {
                        full
                    }
                    image {
                        large
                    }
                }
            }
        }
    }
}
"""


#?----- fetches anime details from AniList API -----?#

@st.cache_data(ttl=3600)
def get_anime_details(anime_id):
    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": ANIME_DETAIL_QUERY,
            "variables": {
                "id": anime_id,
            },
        },
        timeout=15,
    )

    if not response.ok:
        print("ANILIST STATUS:", response.status_code)
        print("ANILIST RESPONSE:", response.text)
        raise RuntimeError(
            f"AniList request failed: {response.text}"
        )

    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    return payload["data"]["Media"]


EXPLORE_ANIME_QUERY = """
query (
    $page: Int,
    $perPage: Int,
    $genre: String,
    $seasonYear: Int,
    $season: MediaSeason,
    $sort: [MediaSort]
) {
    Page(page: $page, perPage: $perPage) {
        media(
            type: ANIME
            isAdult: false
            genre: $genre
            seasonYear: $seasonYear
            season: $season
            sort: $sort
        ) {
            id

            title {
                english
                romaji
            }

            coverImage {
                extraLarge
                large
            }

            bannerImage
            averageScore
            episodes
            genres
            season
            seasonYear
            status
            description(asHtml: false)
        }
    }
}
"""



def fetch_anime(sort, per_page=20):
    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": ANIME_QUERY,
            "variables": {
                "page": 1,
                "perPage": per_page,
                "sort": sort,
            },
        },
        timeout=15,
    )

    response.raise_for_status()
    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(payload["errors"][0]["message"])

    return payload["data"]["Page"]["media"]

@st.cache_data(ttl=3600)
def get_trending_anime(per_page=20):
    return fetch_anime(["TRENDING_DESC"], per_page)

@st.cache_data(ttl=3600)
def get_popular_anime(per_page=20):
    return fetch_anime(["POPULARITY_DESC"], per_page)


def get_new_releases(per_page=20):
    return fetch_anime(
        ["START_DATE_DESC"],
        per_page,
    )
    
    
ANIME_SEARCH_QUERY = """
query ($search: String, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        media(
            search: $search
            type: ANIME
            isAdult: false
            sort: SEARCH_MATCH
        ) {
            id

            title {
                english
                romaji
            }

            coverImage {
                extraLarge
                large
            }

            bannerImage
            averageScore
            episodes
            genres
            seasonYear
            status
            description(asHtml: false)
        }
    }
}
"""


@st.cache_data(ttl=1800)
def search_anime(search_text, per_page=20):
    search_text = search_text.strip()

    if not search_text:
        return []

    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": ANIME_SEARCH_QUERY,
            "variables": {
                "search": search_text,
                "page": 1,
                "perPage": per_page,
            },
        },
        timeout=15,
    )

    if not response.ok:
        raise RuntimeError(
            f"AniList search failed: {response.text}"
        )

    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    return payload["data"]["Page"]["media"]    
    


@st.cache_data(ttl=3600)
def explore_anime(
    genre=None,
    year=None,
    season=None,
    sort="POPULARITY_DESC",
    page=1,
    per_page=20,
):
    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": EXPLORE_ANIME_QUERY,
            "variables": {
                "page": page,
                "perPage": per_page,
                "genre": genre,
                "seasonYear": year,
                "season": season,
                "sort": [sort],
            },
        },
        timeout=15,
    )

    if not response.ok:
        raise RuntimeError(
            f"AniList Explore request failed: {response.text}"
        )

    payload = response.json()

    if payload.get("errors"):
        raise RuntimeError(
            payload["errors"][0]["message"]
        )

    return payload["data"]["Page"]["media"]


