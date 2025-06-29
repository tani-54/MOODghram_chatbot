import os
import json
import requests
import datetime
import random

def fetch_youtube_shorts(query, max_results=5):
    config_path = os.path.join(os.path.dirname(__file__), "..", "reels_data.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError("reels_data.json not found!")

    with open(config_path, "r") as f:
        config = json.load(f)

    api_key = config.get("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YouTube API key not found in reels_data.json")

    # Add freshness and variety
    days_back = random.randint(0, 14)
    published_after = (datetime.datetime.utcnow() - datetime.timedelta(days=days_back)).isoformat("T") + "Z"

    # Mood-specific query improvement
    mood_queries = {
        "happy": "funny trending comedy shorts",
        "sad": "emotional sad breakup shorts",
        "motivated": "motivational speech hustle shorts",
        "relaxed": "chill lofi music relaxing shorts",
        "angry": "funny rage fails shorts"
    }
    query = mood_queries.get(query.lower(), f"{query} shorts")

    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 10,
        "order": random.choice(["date", "relevance", "viewCount"]),
        "publishedAfter": published_after,
        "videoDuration": "short",
        "safeSearch": "strict",
        "key": api_key
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    results = response.json()
    videos = []

    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/embed/{video_id}"
        videos.append({"title": title, "video_url": video_url})

    random.shuffle(videos)
    return videos[:max_results]
