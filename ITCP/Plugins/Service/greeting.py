from telegram import Update , ChatPermissions , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from Database import LOGO , GREETING_TEXT
import asyncio

async def greeting_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(greeting_message_task(update,context))

async def greeting_message_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_id = update.message.message_id
        chat_id=update.effective_chat.id
        updatex = update.message.api_kwargs
    except:return
    try:status,user_id,first_name = [key for key, value in updatex.items()][0] , [value['id'] for key, value in updatex.items()][0] , [value['first_name'] for key, value in updatex.items()][0]
    except:return

    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
      
    if status == 'new_chat_participant':
        chat = await context.bot.get_chat(chat_id=update.effective_chat.id)
        try:
            msg = await context.bot.send_photo(chat_id=update.effective_chat.id,photo=LOGO,caption=GREETING_TEXT.format(user_id,first_name,chat.title),parse_mode="HTML")
            await asyncio.sleep(120)
            await context.bot.delete_message(chat_id=update.effective_chat.id,message_id=msg.message_id)
        except:
            pass 
    if status == 'left_chat_participant':
        pass
