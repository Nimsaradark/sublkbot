from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ContextTypes , CallbackContext 
import asyncio

from Plugins.Manage_files import manage_translate_subs_func

async def handle_documents_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(handle_documents_task(update,context))

async def handle_documents_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manage_translate_subs_func(update,context)
