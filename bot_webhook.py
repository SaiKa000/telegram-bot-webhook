from flask import Flask, request
import telegram

# Token do seu bot
TOKEN = '7655897217:AAGHiUNcvd_vQEQZ4VAEa7d9GZxHh1-PU0s'
bot = telegram.Bot(token=TOKEN)

# Inicia o Flask
app = Flask(__name__)

# Rota principal para verificar se está no ar
@app.route('/')
def index():
    return 'Bot está rodando!'

# Rota que o Telegram vai acessar (webhook)
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message:
        chat_id = update.message.chat.id
        bot.send_message(chat_id=chat_id, text="✅ Bot ativo no Render!")
    
    return 'ok'
