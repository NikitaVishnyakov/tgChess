from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from config import BOT_TOKEN

API_TOKEN = BOT_TOKEN

def start(update, context):
    update.message.reply_text('Welcome to Chess Bot! Type /newgame to start.')

def new_game(update, context):
    game_id = str(update.message.chat.id)
    response = requests.post('http://127.0.0.1:5000/start_game', json={'game_id': game_id})
    if response.status_code == 200:
        update.message.reply_text('New game started! Make a move (e.g., e2e4).')
    else:
        update.message.reply_text('Failed to start game.')

def move(update, context):
    game_id = str(update.message.chat.id)
    move = update.message.text.strip()
    response = requests.post('http://127.0.0.1:5000/make_move', json={'game_id': game_id, 'move': move})
    if response.status_code == 200:
        fen = response.json().get('fen')
        update.message.reply_text(f'Move accepted. Current board:\n{fen}')
    else:
        update.message.reply_text(response.json().get('error'))

updater = Updater(API_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('newgame', new_game))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, move))

updater.start_polling()
updater.idle()
