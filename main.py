# main.py
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

import config
from handlers.start_handler import start
from handlers.search_handler import handle_search, button_callback_handler
from utils.database import get_sheet_data

# --- Basic Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Flask App for Render Health Check ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Rise Anime Bot is alive!"

def run_flask():
    # Use 0.0.0.0 to be accessible externally
    app.run(host='0.0.0.0', port=8080)

# --- Main Bot Logic ---
def main() -> None:
    """Start the bot."""
    logger.info("🚀 Starting Rise Anime Bot...")

    # Initial sync with Google Sheets
    get_sheet_data(force_refresh=True)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.BOT_TOKEN).build()

    # --- Register Handlers ---
    # On /start command
    application.add_handler(CommandHandler("start", start))
    
    # On text messages (for searching)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))

    # On callback queries from inline buttons
    application.add_handler(CallbackQueryHandler(button_callback_handler))

    # --- Run Flask app in a separate thread ---
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    logger.info("🌐 Flask health check endpoint started at http://0.0.0.0:8080")
    
    # --- Start the Bot ---
    # Run the bot until the user presses Ctrl-C
    logger.info("✅ Bot is polling for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()