
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 
""" Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text"""            """ Dont Remove '{' or '}' in text""" 

                           
import os

"""Get Bot Token from @BotFather"""
TOKEN = os.environ.get('5295489145:AAGseaJLasxpp4bUqtkYqwovJX3pnV4hrmA')

"""Other-Details"""
LOGS_CHAT = -1001952943899
LOGO = 'https://graph.org/file/b0a679a33645a2470521d.jpg'
start_img = 'https://graph.org/file/b0a679a33645a2470521d.jpg'

start_caption ="""
<b>✨️ Hey {},
    
<blockquote>Mʏ Nᴀᴍᴇ Is {} ©️</blockquote>
    
📖️ Find & download subtitles for movies & shows in Telegram, Fast, reliable, & easy to use! Try now !</b>
"""


#search results
buttons_per_line = 3

# language code must be in normal font , you can change font of language name
languages = {
    "zh" : "chinese",
    "pt" : "portuguese",
    "ja" : "japanese",
    "en" : "english"  
}
lg_button_per_line = 2 

# language code must be in normal font , you can change font of language name
translatetion_langs = {
    "ml": "Malayalam",
    "ta": "Tamil",
    "hi": "Hindi",
    "kn": "Kannada",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "or": "Odia",
    "bn": "Bengali",
    "pa": "Punjabi",
    "fa": "Persian",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "ru": "Russian",
    "iw": "Hebrew",
    "ar": "Arabic",
    "si": "Sinhala"
}
tr_button_per_line = 3

# transating status message , don't remove or change place of '{}' parts
progress_caption = """<b>Tʀᴀɴꜱʟᴀᴛɪɴɢ To {}...</b>\n
<b>╭━━━━━━━━━━━━━━━➣</b>
<b>┣⪼ | {}</b>
<b>┣⪼ | ᴘᴇʀᴄᴇɴᴛᴀɢᴇ : <code>{} %</code></b>
<b>┣⪼ | Sᴩᴇᴇᴅ : <code>{} Lines/S</code></b>
<b>┣⪼ | Eʟᴀᴘꜱᴇᴅ : <code>{}</code></b>
<b>┣⪼ | Eᴛᴀ : <code>{}</code></b>
<b>╰━━━━━━━━━━━━━━━➣</b>"""
eta_text = (
    "**File name :** `{}`\n**Done** `{}` **of** `{}`\n**Percentage:** {}%\n**Speed:** {} lines/sec\n**ETA:** {}\n[{"
    "}{}] "
)

progress_fill = "⬢"
progress_pending = "⬡"


GREETING_TEXT = """
<b>Hᴇʏ <a href="tg://user?id={}">{}</a>✨️</b>
    
<b><blockquote>Welcome To: {}</blockquote></b>
    
<b>Find & download subtitles for movies & shows in Telegram, Try now !</b>
"""

