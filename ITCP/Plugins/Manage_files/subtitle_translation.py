from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , InputFile , InputMedia
from telegram.ext import ContextTypes , CallbackContext 
from deep_translator import GoogleTranslator
import asyncio
import time
import math
import os 
import io
import re

from Database import progress_caption , eta_text , progress_fill , progress_pending , thumbnail , translatetion_langs ,tr_button_per_line

user_tasks = {}

async def manage_translate_subs_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(manage_translate_subs_task(update,context))

async def manage_translate_subs_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    exten = str(message.document.file_name).split(".")[-1]
    if exten not in ["vtt", "srt","stl","sbv","sub","ass"]:
        return
    user_id = update.effective_user.id
    langs = []
    for language_code , Language in translatetion_langs.items():
        langs.append(InlineKeyboardButton("{} ({})".format(Language.title(),language_code) , callback_data=f"tr:{language_code}:{user_id}"))
    keyboard = []
    buttons = [langs[i:i + tr_button_per_line] for i in range(0, len(langs), tr_button_per_line)]
    for button in buttons:
        keyboard.append(button)
    caption = 'Select a Language what you want to translate'
    await update.message.reply_photo(photo='https://telegra.ph/file/da1ed7494c9af8f15a99f.png',caption=caption,reply_markup=InlineKeyboardMarkup(keyboard),reply_to_message_id=update.effective_message.id)

def format_time(elapsed):
    """Formats elapsed seconds into a human readable format."""
    hours = int(elapsed / (60 * 60))
    minutes = int((elapsed % (60 * 60)) / 60)
    seconds = int(elapsed % 60)
    rval = ""
    if hours:
        rval += "{0}h ".format(hours)
    if elapsed > 60:
        rval += "{0}m ".format(minutes)
    rval += "{0}s ".format(seconds)
    return rval

def get_language_name(code):
    for lang_code ,  language in translatetion_langs.items():
        if lang_code == code:
            return language

 

async def start_translate_func(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.from_user.id in user_tasks and not user_tasks[query.from_user.id].done():
        await query.answer("There is already a translation task running.",show_alert=True)
        return
        
    task = asyncio.create_task(start_translate_task(update,context))
    user_tasks[query.from_user.id] = task
    
async def start_translate_task(update: Update, context: CallbackContext):
    then = time.time()
    query = update.callback_query
    button = query.data
    data = button.split(":")
    lang = data[1]
    
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    lang_str = get_language_name(lang)
    message = query.message.reply_to_message
    exten = str(message.document.file_name).split(".")[-1]
    await query.edit_message_caption("downloading File...")
    user_doc = await message.document.get_file()
    location = os.path.join("./FILES", str(user_id))
    if not os.path.isdir(location):
        os.makedirs(location)
    doc = await user_doc.download_to_drive(location + "/" + message.document.file_name)
    outfile = str(doc).replace(f".{exten}",f'_{lang}.{exten}')
    await query.edit_message_caption(caption=progress_caption.format(lang_str,"⬡⬡⬡⬡⬡⬡⬡⬡","0.00","0","0 s","0H"),parse_mode='HTML')

    process_failed = False
    x = 0
    try:
        print("pass 03")
        with io.open(doc, "r", encoding="utf-8") as file:
            try:
                subtitle = file.readlines()
                print(len(subtitle))
            except Exception:
                query.edit_message_caption("Unsupported characters in file")
                os.remove(doc)
                os.remove(outfile)
                return

            subtitle[0] = "1\n"
            print("pass 04")
            try:
                with io.open(outfile, "x", encoding="utf-8") as f:
                    total = len(subtitle)
                    done = 0
                    for i in range(total):
                        diff = time.time() - then
                        if subtitle[i][0].isdigit() or '-->' in subtitle[i]:
                            f.write("" + str(subtitle[i]))
                            done += 1
                        else:
                            try:
                                if '<' in subtitle[i]:
                                    text_tr = re.search(r'>(.*?)<', subtitle[i]).group(1)
                                    try:translated = GoogleTranslator(source='auto', target=lang).translate(text_tr) 
                                    except:translated = text_tr
                                    html = re.sub(r'>(.*?)<', '>{}<', subtitle[i])
                                    f.write(html.format(translated) + "\n")
                                else:
                                    text_tr = subtitle[i]
                                    try:translated = GoogleTranslator(source='auto', target=lang).translate(text_tr) 
                                    except:translated = text_tr
                                    f.write(translated + "\n")
                                percentage = round(done * 100 / total, 2)
                                
                                done += 1
                                
                                if done % 50 == 0 or x == 0:
                                    x = x + 1
                                    print(user_id," : ",percentage,"%")
                                    try:
                                        keyboard = [[InlineKeyboardButton("Cancel Task", callback_data=f"cancel:{user_id}")]]
                                        progress = f"""{"".join([progress_fill for i in range(math.floor(percentage / 7))])}{"".join([progress_pending for i in range(14 - math.floor(percentage / 7))])} """
                                        await query.edit_message_caption(caption=progress_caption.format(lang_str,progress,percentage,round(done/diff,2),format_time(int(diff)),format_time(int((total - done) / (done/diff)))),parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
                                    except Exception as e:
                                        print(f"Error in send Status: {e}")
                                        pass
                            except Exception:
                                pass
            except Exception as e:
                    print("Error",e)
                    
                    print("pass 05")            
                    speed = done / diff
                    percentage = round(done * 100 / total, 2)
                    eta = format_time(int((total - done) / speed))
                    if done % 20 == 0:
                        try:
                            query.edit_message_caption(
                                caption=eta_text.format(
                                    message.document.file_name,
                                    done,
                                    total,
                                    percentage,
                                    round(speed),
                                    eta,
                                    "".join(
                                        [
                                            "⬢"
                                            for i in range(
                                                math.floor(percentage / 7)
                                            )
                                        ]
                                    ),
                                    "".join(
                                        [
                                            "⬡"
                                            for i in range(
                                                14 - math.floor(percentage / 7)
                                            )
                                        ]
                                    ),
                                )
                            )
                        except Exception:
                            pass
    except Exception as e:
        await query.edit_message_caption(f"Some errors happened Try again...\n\nError : {e}")
        process_failed = True

    print("pass 06")
    if process_failed is not True:
        await query.edit_message_caption(f"Uploading {str(message.document.file_name).replace(exten,f'_{lang}.{exten}')}")
        if os.path.exists(outfile):
            caption = "<b><i>{}_{}.srt</i></b>\n\nTranslated by {}\n\nElapsed : {}"

            try:msg = await context.bot.send_document(document=outfile,chat_id=-1002051680690,thumbnail=thumbnail)
            except Exception as e:
                await query.edit_message_caption(f"Error while Uploading...\n{str(e)}")
                try:
                    os.remove(doc)
                    os.remove(outfile)
                except:
                    pass
                return
            try:
                media = InputMedia(media_type='document',media=msg.document.file_id,caption=caption.format(str(message.document.file_name).replace("srt",""),lang,(await context.bot.get_me()).first_name,format_time(diff)),parse_mode="HTML")
                await query.edit_message_media(media=media)
            except Exception as e:
                print(e)
        else:
            pass
    os.remove(doc)
    os.remove(outfile)


async def cancel_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    if user_id in user_tasks:
        task = user_tasks[user_id]
        try:
            task.cancel()
            await query.answer("Translation task cancelled.",show_alert=True)
            await query.message.delete()
            await context.bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.reply_to_message.message_id)
        except Exception as e:
            await query.answer(e,show_alert=True)
    else:
        await query.answer("No running translation task to cancel.",show_alert=True)


