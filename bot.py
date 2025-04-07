import logging
import os
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from wb_api import get_stock_data
from analyzer import analyze_stock

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_USER_ID:
        return
    await update.message.reply_text("Привет! Я бот для анализа остатков на Wildberries. Напиши /analyze")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_USER_ID:
        return

    data = get_stock_data()

    if not data:
        await update.message.reply_text("❗️Нет данных для анализа.")
    else:
        preview = str(data)[:4000]
        await update.message.reply_text("Ответ WB API:\n" + preview)

    result = analyze_stock(data)
    await update.message.reply_text(result)

async def set_commands(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("analyze", "Показать анализ остатков")
    ])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    app.post_init = set_commands

    app.run_polling()

if __name__ == "__main__":
    main()
