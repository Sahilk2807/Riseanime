# utils/shortener.py
import requests
from config import GPLINKS_API

def shorten_link(url):
    """Shortens a URL using GPLinks API."""
    if not GPLINKS_API:
        return url # Return original URL if no API key is set

    api_url = f"https://gplinks.in/api?api={GPLINKS_API}&url={url}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data.get("shortenedUrl")
        else:
            print(f"GPLinks Error: {data.get('message')}")
            return url
    except requests.RequestException as e:
        print(f"Error shortening link: {e}")
        return url # Return original link on failure