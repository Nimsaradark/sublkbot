from telegram import Update
from telegram.ext import ContextTypes 
from Plugins.Manage_files import manage_download_subtitles

async def handle_text_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        await manage_download_subtitles(update,context)
