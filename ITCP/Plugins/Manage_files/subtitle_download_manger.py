from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , InputMedia , InputFile
from telegram.ext import CallbackContext , ContextTypes
from Plugins.WebSearch import get_result_for_search_term_from_baiscope , get_subtitle_from_baiscope_by_id , get_result_for_search_term_from_zoomlk , get_subtitle_from_zoomlk_by_date , get_download_link_from_zoomlk , get_result_from_opensubtitles , get_subtitle_by_file_id_from_opensubtitle 
from Database import thumbnail , languages ,lg_button_per_line , buttons_per_line
from bs4 import BeautifulSoup
import re
import asyncio
import requests
import zipfile
import rarfile
import shutil
import os

async def create_message_buttons_for_baiscope(search_tearm, user_id):
    subtitles = get_result_for_search_term_from_baiscope(search_tearm)
    keyboard = []
    titles  = ''
    subtitles = [subtitles[i:i + buttons_per_line] for i in range(0, len(subtitles), buttons_per_line)]
    x = 0
    if subtitles:
        for subs in subtitles[0:5] if len(subtitles) > 5 else subtitles:
            buttons = []
            for sub in subs:
                x = x + 1
                post_id= str(sub).split(':')[0]
                title = sub.replace(f"{post_id}:",'').replace("\n","")
                titles += "\n\n<b><blockquote>{}. {}</blockquote></b>".format(x,title.replace("සිංහල උපසිරැසි සමඟ",""))
                buttons.append(InlineKeyboardButton(x, callback_data=f"s_bc:{post_id}:{user_id}"))
            keyboard.append(buttons)
        text = "<blockquote><a href='https://www.baiscope.lk'>Results from Baiscope.lk</a></blockquote>" + titles
    else:
        text = "<blockquote><a href='https://www.baiscope.lk'>Results from Baiscope.lk</a></blockquote>\n\nNo result found"
        keyboard = []
    keyboard.append([InlineKeyboardButton("Click the buttons below to get other results", callback_data="pressed")])
    keyboard.append([InlineKeyboardButton(" Baiscope ", callback_data="pressed"),InlineKeyboardButton(" Zoom lk ", callback_data=f"sh_zlk:{user_id}"),InlineKeyboardButton("Other", callback_data=f"sh_op:{user_id}")])
    return text , keyboard

async def manage_download_subtitles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(manage_download_subtitles_task(update,context))
async def manage_download_subtitles_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(text="searching...",reply_to_message_id=update.message.message_id)
    search_tearm = update.message.text
    user_id = update.effective_user.id
    text , keyboard = await create_message_buttons_for_baiscope(search_tearm,user_id)
    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard),parse_mode='HTML',disable_web_page_preview=True)


async def back_to_baiscope(update: Update, context: CallbackContext):
    asyncio.create_task(back_to_baiscope_task(update,context))
async def back_to_baiscope_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    
    await query.edit_message_text("Searching...")
    search_term = query.message.reply_to_message.text
    text , keyboard = await create_message_buttons_for_baiscope(search_term,user_id)
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard),parse_mode='HTML',disable_web_page_preview=True)


def keyboard_for_opensubs_lang(user_id):
    temp = []
    keyboard = []
    for language_code, language in languages.items():
        temp.append(InlineKeyboardButton("{} ({})".format(language.title(),language_code), callback_data=f"opsb:{language_code}:{user_id}"))
    buttons = [temp[i:i + lg_button_per_line] for i in range(0, len(temp), lg_button_per_line)]
    for button in buttons:
        keyboard.append(button)
    keyboard.append([InlineKeyboardButton("Back", callback_data=f"b2b:{user_id}")])
    return keyboard


async def change_to_opensubtitles_laguages(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_opensubtitles_laguages_task(update,context))
async def change_to_opensubtitles_laguages_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
        
    text = "<b><i>Select language what you want</i></b>"
    keyboard = keyboard_for_opensubs_lang(user_id)
    reply_markup =  InlineKeyboardMarkup(keyboard)
    await  query.edit_message_text(text=text, reply_markup=reply_markup,parse_mode='HTML',disable_web_page_preview=True)



async def change_to_opensubtitles(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_opensubtitles_task(update,context))
async def change_to_opensubtitles_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    await query.edit_message_text("Searching...")
    search_term = query.message.reply_to_message.text
    lang = data[-2]
    subtitles = get_result_from_opensubtitles(search_term,lang)
    keyboard = []
    titles = ''
    if subtitles:
        x = 0
        subtitles = [subtitles[i:i + buttons_per_line] for i in range(0, len(subtitles), buttons_per_line)]
        for subs in subtitles[0:5] if len(subtitles) > 5 else subtitles:
            buttons = []
            for sub in subs:
                x = x + 1
                data = sub.split("b:")
                file_id = data[-1]
                title = data[0]
                titles += "\n\n<b><blockquote>{}. {}</blockquote></b>".format(x,(title).replace("."," "))
                buttons.append(InlineKeyboardButton(x, callback_data=f"ens_d:{file_id}:{update.effective_user.id}"))
            keyboard.append(buttons)
        keyboard.append([InlineKeyboardButton("Click the buttons below to get other results", callback_data="pressed")])
        keyboard.append([InlineKeyboardButton(" Baiscope ", callback_data=f"b2b:{update.effective_user.id}"),InlineKeyboardButton(" Zoom lk ", callback_data=f"sh_zlk:{user_id}"),InlineKeyboardButton(" Opensubtitles ", callback_data="pressed")])
        keyboard.append([InlineKeyboardButton("Back", callback_data=f"sh_op:{update.effective_user.id}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "<blockquote><a href='https://zoom.lk'>Results from opensubtitles.org</a></blockquote>" + titles
        await  query.edit_message_text(text=text, reply_markup=reply_markup,parse_mode='HTML',disable_web_page_preview=True)
    else:
        keyboard = keyboard_for_opensubs_lang(user_id)
        reply_markup =  InlineKeyboardMarkup(keyboard)
        text = "<b><i>No result Found </i></b>"
        await  query.edit_message_text(text=text, reply_markup=reply_markup,parse_mode='HTML',disable_web_page_preview=True)

async def download_sub_from_opensubtitles(update: Update, context: CallbackContext):
    asyncio.create_task(download_sub_from_opensubtitles_task(update,context))
async def download_sub_from_opensubtitles_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    file_id = data[1]
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    await query.answer()
    msg = await context.bot.send_message(chat_id=query.message.chat.id,text="Processing...")
    post_id = button.split(':')[1]
    search_term = query.message.reply_to_message.text
    try:
        await msg.edit_text("Downloading...")
        file_name , subtitle_id = get_subtitle_by_file_id_from_opensubtitle(search_term,file_id)
        # await msg.edit_text(f"Uploading...\nFile name : {file_name}\nUrl : {url}")
        doc = downloadSubtitles(file_id , subtitle_id, file_name)
        if doc == None:
            error_msg = """
<b><i>Download from www.opensubtitles.org limit reached !</i></b> 
<b><i>Try Again Later !</i></b> 
"""
            await msg.edit_text(text=error_msg,parse_mode="HTML")
            await asyncio.sleep(5)
            await msg.delete()
            return
            
        # fileinput = InputFile(obj=doc,filename=f"{file_name}.srt")
        await msg.edit_text("Uploading...")
        # ,thumbnail=thumbnail
        msg2 = await context.bot.send_document(document=doc,chat_id=query.message.chat.id,thumbnail=thumbnail)
        await context.bot.edit_message_caption(chat_id=query.message.chat.id,message_id=msg2.message_id,caption=f"<b><i>{str(msg2.document.file_name)}</i></b>",parse_mode='HTML')
        os.remove(doc)
        await msg.delete()
        # out_file = download_sub_from_opensubtitles(url,f"{file_name}.srt")
    except Exception as e:
        await msg.edit_text("Error : ",e)
        await asyncio.sleep(5)
        await msg.delete()
        print("Error in get download link",e)
    try:shutil.rmtree(f"./FILES/{subtitle_id}")
    except:pass   

async def change_to_zoomlk(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_zoomlk_task(update,context))
async def change_to_zoomlk_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    await query.edit_message_text("Searching...")
    search_term = query.message.reply_to_message.text
    subtitles = get_result_for_search_term_from_zoomlk(search_term)
    keyboard = []
    titles = ''
    if subtitles:
        x = 0
        subtitles = [subtitles[i:i + buttons_per_line] for i in range(0, len(subtitles), buttons_per_line)]
        for subs in subtitles[0:5] if len(subtitles) > 5 else subtitles:
            buttons = []
            for sub in subs:
                x = x + 1
                link= str(sub).split('b:')[0]
                date = str(sub).split('b:')[-1]
                title = str(sub).replace(f"{link}b:","").replace(f"b:{date}","")
                titles += "\n\n<b><blockquote>{}. {}</blockquote></b>".format(x,title.replace("(සිංහල උපසිරැසි)",""))
                buttons.append(InlineKeyboardButton(x, callback_data=f"s_zlkb:{date}b:{update.effective_user.id}"))
            keyboard.append(buttons)
        keyboard.append([InlineKeyboardButton("Click the buttons below to get other results", callback_data="pressed")])
        keyboard.append([InlineKeyboardButton(" Baiscope ", callback_data=f"b2b:{update.effective_user.id}"),InlineKeyboardButton(" Zoom lk ", callback_data="pressed"),InlineKeyboardButton("Other", callback_data=f"sh_op:{update.effective_user.id}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "<blockquote><a href='https://zoom.lk'>Results from Zoom.lk</a></blockquote>" + titles
        await  query.edit_message_text(text=text, reply_markup=reply_markup,parse_mode='HTML',disable_web_page_preview=True)
    else:
         keyboard.append([InlineKeyboardButton(" Baiscope ", callback_data=f"b2b:{update.effective_user.id}"),InlineKeyboardButton(" Zoom lk ", callback_data="pressed"),InlineKeyboardButton("Other", callback_data=f"sh_op:{update.effective_user.id}")])
         reply_markup = InlineKeyboardMarkup(keyboard)
         text = "<b><i>No result found</i></b>"
         await  query.edit_message_text(text=text, reply_markup=reply_markup,parse_mode='HTML',disable_web_page_preview=True)





async def download_sub_from_baiscope(update: Update, context: CallbackContext):
    asyncio.create_task(download_sub_from_baiscope_task(update,context))
async def download_sub_from_baiscope_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    await query.answer()
    msg = await context.bot.send_message(chat_id=query.message.chat.id,text="Processing...")
    post_id = button.split(':')[1]
    search_term = query.message.reply_to_message.text
    downlaod_link = get_subtitle_from_baiscope_by_id(search_term,post_id)
    try:filename = (str(downlaod_link).split('/')[4])+ '.zip'
    except:filename = "sub.zip"
    filename = filename.replace("_-zip",'')
    if downlaod_link:
        await msg.edit_text("Downloading...")
        outfile = download_file(downlaod_link, filename,user_id)
        if outfile:
            try:
                sub_files = extract_files(outfile,f"./FILES/{user_id}")
                # (obj='test3.py', filename='test3.py')
                
                await msg.edit_text("Uploading...")
                for sub_file in sub_files:
                    filename = str(sub_file).split("/")[-1]
                    if filename.endswith(".srt") or filename.endswith(".vtt") or filename.endswith(".sbv") or filename.endswith(".sub") or filename.endswith(".ass"): 
                        # fileinput = InputFile(obj=sub_file,filename=filename)
                        # ,thumbnail=thumbnail
                        msg2 = await context.bot.send_document(document=sub_file,chat_id=query.message.chat.id,thumbnail=thumbnail)
                        keyboard = [[InlineKeyboardButton("Direct Download", url=downlaod_link)]]
                        await context.bot.edit_message_caption(chat_id=query.message.chat.id,message_id=msg2.message_id,caption=f"<b><i>{str(msg2.document.file_name)}</i></b>",parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
                    else:
                        pass
            except:
                msg2 = await context.bot.send_document(document=outfile,chat_id=query.message.chat.id,thumbnail=thumbnail)
                keyboard = [[InlineKeyboardButton("Direct Download", url=downlaod_link)]]
                await context.bot.edit_message_caption(chat_id=query.message.chat.id,message_id=msg2.message_id,caption=f"<b><i>{str(msg2.document.file_name)}</i></b>",parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
    
    await msg.delete()
    try:shutil.rmtree(f"./FILES/{user_id}")
    except:pass
                    
            
async def download_sub_from_zoomlk(update: Update, context: CallbackContext):
    asyncio.create_task(download_sub_from_zoomlk_task(update,context))
async def download_sub_from_zoomlk_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split("b:")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    await query.answer()
    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    text_lines = (query.message.text).split("\n")
    for i in reply_keyboard:
        for j in i:
            if j.callback_data == button:
                button_text = j.text
    for text_line in text_lines:
        if text_line.startswith(button_text):
            filename = text_line.replace(f"{button_text}.","") + ".rar"
        
    msg = await context.bot.send_message(chat_id=query.message.chat.id,text="Processing...")
    date = data[1]
    search_term = query.message.reply_to_message.text
    link = get_subtitle_from_zoomlk_by_date(search_term,date)
    download_link = get_download_link_from_zoomlk(link)
    if download_link:
        await msg.edit_text("Downloading...")
        outfile = download_file(download_link,filename,user_id)
        if outfile:
            await msg.edit_text("Uploading...")
            try:
                sub_files = extract_files(outfile, f"./FILES/{user_id}")
                for sub_file in sub_files:
                    filename = str(sub_file).split("/")[-1]
                    if filename.endswith(".srt") or filename.endswith(".vtt") or filename.endswith(".sbv") or filename.endswith(".sub") or filename.endswith(".ass"): 
                        # (obj='test3.py', filename='test3.py')
                        # fileinput = InputFile(obj=sub_file,filename=filename)
                        
                        # ,thumbnail=thumbnail
                        msg2 = await context.bot.send_document(document=sub_file,chat_id=query.message.chat.id,thumbnail=thumbnail)
                        keyboard = [[InlineKeyboardButton("Direct Download", url=downlaod_link)]]
                    
                    await context.bot.edit_message_caption(chat_id=query.message.chat.id,message_id=msg2.message_id,caption=f"<b><i>{str(msg2.document.file_name)}</i></b>",parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
                await msg.delete()
            except:   
                # fileinput = InputFile(obj=outfile,filename=filename)
                # ,thumbnail=thumbnail
                msg2 = await context.bot.send_document(document=outfile,chat_id=query.message.chat.id,thumbnail=thumbnail)
                keyboard = [[InlineKeyboardButton("Direct Download", url=download_link)]]
                
                await context.bot.edit_message_caption(chat_id=query.message.chat.id,message_id=msg2.message_id,caption=f"<b><i>{str(msg2.document.file_name)}</i></b>",parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
    await msg.delete()
    try:shutil.rmtree(f"./FILES/{user_id}")
    except:pass   
            

def download_file(url, filename,user_id):
    location = os.path.join("./FILES", str(user_id))
    if not os.path.isdir(location):
        os.makedirs(location)
    
    file_path = location + '/' + filename
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return file_path
    else:
        try:os.remove(file_path)
        except:pass
        return None

def extract_files(file_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    if str(file_path).endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            files = zip_ref.namelist()
            zip_ref.extractall(extract_to)
            return files
    elif str(file_path).endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
            files = rar_ref.namelist()
            return files
    else:
        return None
    
    

def downloadSubtitles(file_id , subtitle_id, file_name):
    sub_down_url = f"https://www.opensubtitles.com/nocache/download/{file_id}/subreq.js?file_name={file_name}&locale=en&np=true&sub_frmt=srt&subtitle_id={subtitle_id}" 
    response = requests.get(sub_down_url)
    location = os.path.join("./FILES",subtitle_id)
    if not os.path.isdir(location):
        os.makedirs(location)
    file_path = location + '/' + file_name + ".srt"
    if response.status_code == 200:
        print("URL : ", sub_down_url)
        results = BeautifulSoup(response.content, "html.parser").find("a")
        pattern = r'"(https:\/\/www.opensubtitles.com\/download\/[^"]+)"'
        download_links = re.findall(pattern, str(results))
        if download_links != []:
            subtitle_link = download_links[0]
            response = requests.get(subtitle_link)
            if response.status_code == 200:
                
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
    return None                

