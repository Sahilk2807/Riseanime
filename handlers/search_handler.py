# handlers/search_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils import tmdb, database, shortener
from templates.message_templates import format_media_details

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's text message to search for media."""
    query = update.message.text
    if len(query) < 3:
        await update.message.reply_text("🤔 Please enter at least 3 letters to start a search.")
        return

    # Send a "thinking" message and show typing animation
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    thinking_message = await update.message.reply_text("⏳ Searching for your anime...")

    search_results = tmdb.search_media(query)

    if not search_results:
        await thinking_message.edit_text("❌ Sorry, I couldn't find any anime or movie with that name.")
        return
    
    # If more than 5 results, limit them to avoid spam
    if len(search_results) > 5:
        search_results = search_results[:5]

    keyboard = []
    for item in search_results:
        media_type = item['media_type']
        item_id = item['id']
        if media_type == 'tv':
            title = item.get('name')
            year = item.get('first_air_date', 'N/A').split('-')[0]
        else:
            title = item.get('title')
            year = item.get('release_date', 'N/A').split('-')[0]
        
        button_text = f"🎬 {title} ({year})"
        callback_data = f"select_{media_type}_{item_id}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await thinking_message.edit_text("🔍 I found a few options. Please select one:", reply_markup=reply_markup)


async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the callback from inline buttons."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    data = query.data
    if data.startswith("select_"):
        _, media_type, media_id = data.split("_")

        # Edit the message to show we're fetching details
        await query.edit_message_text(text="😎 Got it! Fetching details now...")
        await context.bot.send_chat_action(chat_id=query.effective_chat.id, action='typing')

        details = tmdb.get_media_details(media_id, media_type)
        if not details:
            await query.edit_message_text("❌ An error occurred while fetching details.")
            return

        # Find download links from Google Sheets
        download_links = database.find_download_links(details['title'])
        
        # Format the message content
        message_text = format_media_details(details, download_links)
        
        # Create download buttons
        buttons = []
        if download_links:
            for quality, link in download_links.items():
                short_link = shortener.shorten_link(link)
                buttons.append([InlineKeyboardButton(f"📥 Download {quality}", url=short_link)])
        
        reply_markup = InlineKeyboardMarkup(buttons)

        # Delete the "fetching details" message and send the final result with a poster
        await query.message.delete()

        if details['poster_path']:
            await context.bot.send_photo(
                chat_id=query.effective_chat.id,
                photo=details['poster_path'],
                caption=message_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )
        else: # Send as text if no poster
            await context.bot.send_message(
                chat_id=query.effective_chat.id,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )