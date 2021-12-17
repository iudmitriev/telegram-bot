import telebot

with open("bot_control_token.txt", "r") as f:
	token = f.readline()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Welcome!")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "This is simple echo bot.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
