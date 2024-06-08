from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ContextTypes , CallbackContext
import asyncio

from ITZCP_functions import mention_html
from Database import start_caption , start_img

def start_keyboard(bot_username,user_id):
    keyboard = [
        [InlineKeyboardButton("➕ Add Me To Your Chat ➕",url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton('⭕️ Search',switch_inline_query_current_chat=''),InlineKeyboardButton('🔔 Updates',url="t.me/FilmZone_Official")],
        [InlineKeyboardButton('🌸 Status', callback_data=f'status:{user_id}'),InlineKeyboardButton('☘️ About', callback_data=f'about:{user_id}')],
               ]
    return keyboard


async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(start_command_task(update, context))

async def start_command_task(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    sticker = "CAACAgUAAxkBAAErZ7NmQ1PMduw_dLsWbFnlIJ_YmXI16gACBAADwSQxMYnlHW4Ls8gQNQQ"
    msg = await update.message.reply_sticker(sticker)
    mention = await mention_html(user.id,False)
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    await asyncio.sleep(2)
    await msg.delete()

    await update.message.reply_photo(photo=start_img,caption=(start_caption).format(mention,bot_name),parse_mode='html',reply_markup=InlineKeyboardMarkup(start_keyboard(bot_.username,user.id)))

async def back_to_start(update: Update, context: CallbackContext):
    asyncio.create_task(back_to_start_task(update, context))
async def back_to_start_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    mention = await mention_html(user_id,False)
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    await query.edit_message_caption(caption=(start_caption).format(mention,bot_name),parse_mode='html',reply_markup=InlineKeyboardMarkup(start_keyboard(bot_.username,user_id)))
    
async def change_to_about(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_about_task(update, context))
async def change_to_about_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    bot_username = f"<a href='https://t.me/{bot_.username}'>@{bot_.username}</a>"
    caption = f""" 
ᴀʙᴏᴜᴛ ᴍᴇ
┬───────────────────────
├ ɴᴀᴍᴇ : {bot_name}
│ 
├ ᴜsᴇʀɴᴀᴍᴇ : {bot_username}
│ 
├ ᴡʀɪᴛᴛᴇɴ ɪɴ : ᴘʏᴛʜᴏɴ 𝟹.𝟷𝟷
│ 
├ ʟɪʙʀᴀʀɪᴇs : 
│      └ ᴘʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ
│  
├ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/Itzmecp'>Itzmecp</a>      
│ 
└ ᴠᴇʀsɪᴏɴ : ᴠ3.5
"""
    keyboard = [[InlineKeyboardButton(" Back ",callback_data=f"b2s:{user_id}")]]
    await query.edit_message_caption(caption=caption,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
