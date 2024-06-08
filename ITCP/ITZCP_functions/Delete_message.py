import asyncio
from telegram import Bot
from Database import TOKEN

bot = Bot(TOKEN)

async def delete_message(chat_id,message_id,time):
    task = asyncio.create_task(delete_message_task(chat_id,message_id,time))

async def delete_message_task(chat_id,message_id,time):
    await asyncio.sleep(time)
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass
