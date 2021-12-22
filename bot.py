'''
Simple echo bot
'''

import sys
import shutil
import os
import random
import time

import requests
import telebot

token = sys.argv[1]

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    Sends welcome message
    '''
    bot.reply_to(message, "Welcome! Use /help to see commands")

@bot.message_handler(commands=['help'])
def send_help(message):
    '''
    Sends description
    '''
    bot.reply_to(message, "Use /meme to get random meme\nUse /help to see commands list")

def get_image(url, file):
    '''
        Gets image from url and prints it to file
    '''
    response = requests.get(url, stream=True)
    tmp_file = open(file, 'wb+') # pylint: disable=R1732
    shutil.copyfileobj(response.raw, tmp_file)
    del response
    tmp_file.close()

def get_json_with_memes():
    '''
        Gets json with top 100 memes of hot section of /r/memes
    '''
    url = 'https://www.reddit.com/r/memes/hot/.json?limit=100'
    memes_request = requests.get(url, headers={'User-agent': 'dmitriev_bot'})
    memes_json = memes_request.json()

    number_of_tries = 0
    while 'data' not in memes_json and number_of_tries < 5:
        number_of_tries += 1
        time.sleep(5)
        memes_request = requests.get(url)
        memes_json = memes_request.json()

    if number_of_tries >= 5:
        raise ConnectionError("Failed to maintain connection")

    return memes_json

@bot.message_handler(commands=['meme'])
def send_meme(message):
    '''
    Sends random meme from best of /r/memes
    '''
    chat_id = message.chat.id
    number_of_tries = 0

    while number_of_tries < 5:
        tmp_file_address = 'img_' + str(chat_id) + '_' + str(random.randrange(0, 2**32-1)) + '.png'
        try:

            memes_json = get_json_with_memes()
            random_index = random.randrange(0, 100)

            post = memes_json["data"]["children"][random_index]["data"]
            title = post["title"]
            image_url = post["url_overridden_by_dest"]

            get_image(image_url, tmp_file_address)

            if os.path.getsize(os.getcwd() + '/' + tmp_file_address) > 5000000:
                raise ValueError("File is too big")

            with open(tmp_file_address, 'rb') as tmp_file:
                bot.send_message(chat_id, title)
                bot.send_photo(chat_id, tmp_file)
            os.remove(tmp_file_address)
            return

        except Exception: # pylint: disable=W0703
            number_of_tries += 1
            if os.path.exists(tmp_file_address):
                os.remove(tmp_file_address)
    bot.send_message(chat_id, "Something went wrong")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    '''
    Echo message
    '''
    chat_id = message.chat.id
    bot.send_message(chat_id, "Unknown command. Use /help to see commands list")

bot.infinity_polling()
