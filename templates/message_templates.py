# templates/message_templates.py
import re

def escape_markdown(text):
    """Helper function to escape telegram markdown symbols."""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))

def format_media_details(details, download_links):
    """Formats the anime/movie details into a beautiful Markdown message."""
    
    title = escape_markdown(f"{details['title']} ({details['year']})")
    description = escape_markdown(details['description'])
    genres = escape_markdown(", ".join(details['genres']))
    rating = escape_markdown(details['rating'])
    runtime = escape_markdown(details['runtime'])
    release_date = escape_markdown(details['release_date'])

    message = (
        f"🎬 *{title}*\n\n"
        f"📌 *Description:*\n`{description}`\n\n"
        f"🎭 *Genre:* {genres}\n"
        f"⭐ *Rating:* {rating}/10\n"
        f"📅 *Release Date:* {release_date}\n"
        f"⏳ *Runtime:* {runtime}\n\n"
    )

    if download_links:
        message += "📥 *Download Links:*"
    else:
        message += "❌ *No download links found in our database for this title.*"
        
    return message