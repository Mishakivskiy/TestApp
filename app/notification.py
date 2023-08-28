import os
import telebot

from django.conf import settings


def send_telegram_message(message):
    bot_token = settings.BOT_TOKEN
    chat_id = settings.CHAT_ID

    bot = telebot.TeleBot(bot_token)
    bot.send_message(chat_id, message)