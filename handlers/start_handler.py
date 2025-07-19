# handlers/start_handler.py
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    welcome_message = (
        f"👋 Hello, {user.first_name}!\n\n"
        "I am **Rise Anime Bot** 📦, your go-to assistant for finding and downloading anime & movies.\n\n"
        "To get started, simply type at least 3 letters of the anime or movie title you're looking for.\n\n"
        "For example, try typing `one piece` or `jujutsu`."
    )
    await update.message.reply_html(welcome_message)