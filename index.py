import os
import time
from io import BytesIO
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from movies_scraper import search_movies, get_movie
import asyncio
import tracemalloc

TOKEN = os.getenv("TOKEN")
URL = "https://moviesbot-peach.vercel.app"
bot = Bot(TOKEN)
msgid1 = ""
chatid1 = ""



def welcome(update, context) -> None:
    update.message.reply_text(f"Hello *{update.message.from_user.first_name}* \n Welcome To Our Group.\n"
                              f"🔥 Search It 💯  Enjoy it  🍿")
    l = update.message.reply_text("👇 Type Movie Or Series Name 👇")



def find_movie(update, context):
    search_results = update.message.reply_text("🔥 Searching.... Pls Wait..💯")
    query = update.message.text
    chatid = update.message.chat.id
    movies_list = search_movies(query)
    tracemalloc.start()
    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = InlineKeyboardButton(movie["title"], callback_data=movie["id"])
            keyboards.append([keyboard])
        reply_markup = InlineKeyboardMarkup(keyboards)
        m = search_results.edit_text('Here I found - Pls Select One..!', reply_markup=reply_markup)   

    else:
         ok='ok'
       
        
    
    
def movie_result(update, context) -> None:
    query = update.callback_query
    msgid = query.message.message_id
    chatid = query.message.chat.id
    global chatid1
    chatid1 = chatid
    s = get_movie(query.data)
    response = requests.get(s["img"])
    img = BytesIO(response.content)
    m = query.message.reply_photo(photo=img, caption=f"🎥 {s['title']}")
    global msgid1
    msgid1 = m["message_id"]
    link = ""
    links = s["links"]
    keyboards = []
    request = InlineKeyboardButton("Join Our Official Channel", url="https://t.me/fzfilmyzilla")
    keyboards.append([request])
    for i in links:
        t = links[i] + "\n"
        urll = links[i]
        keyboard = InlineKeyboardButton(i, url=urll)
        keyboards.append([keyboard])
    reply_markup = InlineKeyboardMarkup(keyboards)
    k = query.message.reply_text('Click To Watch Online & Download', reply_markup=reply_markup)
    bot.delete_message(chat_id=chatid, message_id=msgid)
    #asyncio.create_task(dlt(chatid1, msgid))
    #loop = asyncio.get_event_loop()
    #task = loop.create_task(dlt(chatid1, msgid))
    #dlt(chatid1, msgid)

 
async def dlt(chid, midd): 
    
     await asyncio.sleep(20)
     bot.delete_message(chat_id=chid, message_id=midd)
   

def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.text, find_movie))
    dispatcher.add_handler(CallbackQueryHandler(movie_result))
    return dispatcher

  
   

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
