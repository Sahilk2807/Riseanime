# utils/database.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from threading import Lock
from config import GOOGLE_CREDS, GOOGLE_SHEET_NAME

# --- Caching Mechanism ---
cache = {
    'data': [],
    'last_updated': 0
}
CACHE_DURATION = 300  # 5 minutes
lock = Lock()

def get_sheet_data(force_refresh=False):
    """Fetches data from Google Sheets, using a cache to avoid rate limits."""
    with lock:
        now = time.time()
        if not force_refresh and (now - cache['last_updated'] < CACHE_DURATION):
            return cache['data']

        print("🔄 Syncing with Google Sheets database...")
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDS, scope)
            client = gspread.authorize(creds)
            sheet = client.open(GOOGLE_SHEET_NAME).sheet1
            
            records = sheet.get_all_records()
            cache['data'] = records
            cache['last_updated'] = now
            print("✅ Database sync complete.")
            return records
        except Exception as e:
            print(f"❌ Error accessing Google Sheets: {e}")
            # Return old cache if sync fails
            return cache['data']

def find_download_links(title):
    """
    Finds download links for a given title from the cached sheet data.
    The search is case-insensitive and partial.
    """
    data = get_sheet_data()
    # Normalize the search title
    search_title_norm = title.lower().strip()
    
    for record in data:
        # Normalize the title from the sheet
        record_title_norm = record.get('Title', '').lower().strip()
        
        if search_title_norm in record_title_norm:
            links = {}
            # Iterates through columns like 'Quality_1', 'Link_1', 'Quality_2', 'Link_2', etc.
            for i in range(1, 10): # Check for up to 9 quality/link pairs
                quality_key = f'Quality_{i}'
                link_key = f'Link_{i}'
                if record.get(quality_key) and record.get(link_key):
                    links[record[quality_key]] = record[link_key]
            return links
            
    return {}