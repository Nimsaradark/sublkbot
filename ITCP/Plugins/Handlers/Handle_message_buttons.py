from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , InputMedia 
from telegram.ext import ContextTypes , CallbackContext

from Plugins.Manage_files import start_translate_func , cancel_task , download_sub_from_baiscope , change_to_zoomlk , back_to_baiscope , download_sub_from_zoomlk , change_to_opensubtitles , download_sub_from_opensubtitles , change_to_opensubtitles_laguages
from Plugins.Commands import back_to_start , change_to_about

async def handle_buttons_func(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    
    if button.startswith("pressed"):
        await query.answer()
        
    if button.startswith('tr'):
        await start_translate_func(update,context)
        
    if button.startswith('cancel'):
        await cancel_task(update,context)
        
    if button.startswith("s_bc"):   
        await download_sub_from_baiscope(update,context)
        
    if button.startswith("sh_zlk"):
        await change_to_zoomlk(update,context)

    if button.startswith("b2b"):
        await back_to_baiscope(update,context)

    if button.startswith("s_zlkb"):
        await download_sub_from_zoomlk(update,context)

    if button.startswith("sh_op"):
        await change_to_opensubtitles_laguages(update,context)

    if button.startswith("opsb"):
        await change_to_opensubtitles(update,context)

    if button.startswith("ens_d"):
        await download_sub_from_opensubtitles(update,context)

    if button.startswith("about"):
        await change_to_about(update,context)

    if button.startswith("b2s"):
        await back_to_start(update,context)
    
