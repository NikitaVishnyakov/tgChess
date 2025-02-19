from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes


# Команда /play
from config import BOT_TOKEN


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # URL вашего хостинга с шахматным приложением
    web_app_url = "https://nikitavishnyakov.github.io/tgChess/"

    # Кнопка запуска Web App
    keyboard = [
        [InlineKeyboardButton("Играть в шахматы", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Нажмите кнопку ниже, чтобы начать игру:", reply_markup=reply_markup)

# Команда /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Игра остановлена. Чтобы начать новую, введите /play.")


# Основной код
def main():
    TOKEN = BOT_TOKEN

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling()


if __name__ == "__main__":
    main()
