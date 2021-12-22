'''
Simple echo bot
'''

import sys
import telebot # pylint: disable=import-error

token = sys.argv[1]

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    Sends welcome message
    '''
    bot.reply_to(message, "Welcome!")

@bot.message_handler(commands=['help'])
def send_help(message):
    '''
    Sends description
    '''
    bot.reply_to(message, "This is still simple echo bot, it will be better")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    '''
    Echo message
    '''
    bot.reply_to(message, message.text)

bot.infinity_polling()