# config.py
import os
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set in the environment variables!")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("❌ TMDB_API_KEY is not set in the environment variables!")

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID is not set in the environment variables!")

GPLINKS_API = os.getenv("GPLINKS_API")

# Load Google Sheets credentials from the environment variable
# The variable should contain the JSON content as a string
google_creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
if not google_creds_json:
    raise ValueError("❌ GOOGLE_SHEETS_CREDENTIALS_JSON is not set!")
try:
    # Parse the JSON string into a dictionary
    GOOGLE_CREDS = json.loads(google_creds_json)
except json.JSONDecodeError:
    raise ValueError("❌ GOOGLE_SHEETS_CREDENTIALS_JSON is not a valid JSON string!")


GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "RiseAnimeDB")