import telebot
import os

TOKEN = '8289028685:AAGmSHEzAIZjjzS5xxbOoCYNGPbpHB7lScU'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً فيك! البوت شغال 24/7 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "كتبت: " + message.text)

print("البوت شغال...")
bot.infinity_polling()
