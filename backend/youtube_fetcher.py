import requests
import json
import os

def fetch_youtube_shorts(query, max_results=5):
    config_path = os.path.join(os.path.dirname(__file__), "..", "reels_data.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    api_key = config.get("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("API key missing in reels_data.json")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{query} shorts",
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
        "videoDuration": "short",
        "safeSearch": "strict"
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    results = response.json()
    videos = []
    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append({
            "title": title,
            "video_url": f"https://www.youtube.com/embed/{video_id}"
        })

    return videos

