from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, CommandHandler
import os
from datetime import datetime

TOKEN = '7655897217:AAGHiUNcvd_vQEQZ4VAEa7d9GZxHh1-PU0s'  # Substitua pelo seu token real
bot = Bot(TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

user_states = {}

def start(update, context):
    update.message.reply_text("Olá! Envie o nome da pasta onde deseja salvar a imagem.")

def handle_text(update, context):
    user_id = update.effective_user.id
    folder_name = update.message.text.strip()
    os.makedirs(folder_name, exist_ok=True)
    user_states[user_id] = folder_name
    update.message.reply_text(f"Fotos serão salvas em: *{folder_name}*", parse_mode="Markdown")

def handle_photo(update, context):
    user_id = update.effective_user.id
    if user_id not in user_states:
        update.message.reply_text("Envie antes o nome da pasta.")
        return

    folder_name = user_states[user_id]
    photo = update.message.photo[-1]
    file = bot.get_file(photo.file_id)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"foto_{now}.jpg"
    filepath = os.path.join(folder_name, filename)
    os.makedirs(folder_name, exist_ok=True)
    file.download(custom_path=filepath)
    update.message.reply_text(f"Imagem salva como *{filename}*", parse_mode="Markdown")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_photo))

@app.route(f"/{7655897217:AAGHiUNcvd_vQEQZ4VAEa7d9GZxHh1-PU0s}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'
