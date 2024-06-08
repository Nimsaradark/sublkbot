from telegram import Bot , Update
from telegram.ext import Application ,ContextTypes , CallbackContext , CommandHandler , MessageHandler , filters , CallbackQueryHandler 
from warnings import filterwarnings
import asyncio
import heroku3
import os

from Database import TOKEN
from Plugins.Commands import (
     start_command
    )
from Plugins.Handlers import (
     handle_documents_func,
     handle_buttons_func,
     handle_text_func
    )
from Plugins.Service import (
     greeting_message
)

HEROKU_API_KEY = os.environ.get('API_KEY',False)
HEROKU_APP_NAME = os.environ.get('APP_NAME',False)
WEB_HOOK_URL = os.environ.get('WEBHOOK',False)
PORT = int(os.environ.get('PORT', '8443'))

filterwarnings(action='ignore', category=DeprecationWarning)

print("Starting bot...")

async def set_webhook(webhook_url):
     bot = Bot(TOKEN)
     await bot.set_webhook(webhook_url + "/" + TOKEN)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    # app.add_handler(CommandHandler("imdb", imdb_details_func))
    # app.add_handler(CommandHandler("cast", broadcast_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, greeting_message)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_func))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_documents_func))
    app.add_handler(CallbackQueryHandler(handle_buttons_func))

    app.add_error_handler(error)
    if (HEROKU_API_KEY!= False and HEROKU_APP_NAME != False) or WEB_HOOK_URL != False:
         loop = asyncio.get_event_loop()
         if HEROKU_API_KEY!= False and HEROKU_APP_NAME != False:     
              heroku_conn = heroku3.from_key(HEROKU_API_KEY)
              happ = heroku_conn.apps()[HEROKU_APP_NAME]
              WEB_HOOK_URL = str(happ.domains()[0]).replace("<domain ","").replace(">","").replace("'","") + "/"
         loop.run_until_complete(set_webhook(WEB_HOOK_URL))
         print('Running Webhook...')
         app.run_webhook(port=PORT,listen="0.0.0.0",webhook_url=WEB_HOOK_URL)
    else:
        print('Polling...')
        app.run_polling()
