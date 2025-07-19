# utils/tmdb.py
import requests
from config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def search_media(query):
    """Searches for TV shows (anime) and movies on TMDb."""
    search_url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": False
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        # Filter for TV shows and Movies only
        return [item for item in results if item.get('media_type') in ['tv', 'movie']]
    except requests.RequestException as e:
        print(f"Error searching TMDb: {e}")
        return []

def get_media_details(media_id, media_type):
    """Gets detailed information for a specific TV show or movie."""
    detail_url = f"{BASE_URL}/{media_type}/{media_id}"
    params = {"api_key": TMDB_API_KEY}
    try:
        response = requests.get(detail_url, params=params)
        response.raise_for_status()
        details = response.json()
        
        # Normalize data between TV and Movie
        if media_type == 'tv':
            title = details.get('name')
            release_date = details.get('first_air_date', 'N/A')
            runtime = details.get('episode_run_time', [0])[0] if details.get('episode_run_time') else 'N/A'
        else: # movie
            title = details.get('title')
            release_date = details.get('release_date', 'N/A')
            runtime = details.get('runtime', 'N/A')

        return {
            "id": details.get('id'),
            "title": title,
            "description": details.get('overview', 'No description available.'),
            "poster_path": f"{IMAGE_BASE_URL}{details.get('poster_path')}" if details.get('poster_path') else None,
            "genres": [genre['name'] for genre in details.get('genres', [])],
            "rating": f"{details.get('vote_average', 0):.1f}",
            "release_date": release_date,
            "year": release_date.split('-')[0] if release_date != 'N/A' else 'N/A',
            "runtime": f"{runtime} min" if isinstance(runtime, int) else runtime,
            "media_type": media_type
        }
    except requests.RequestException as e:
        print(f"Error getting TMDb details: {e}")
        return None