import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from threading import Thread
from flask import Flask

TOKEN = os.getenv("TOKEN", "8525467586:AAFAmrbV-HMV36NOwOLLU3zKrT_UwnSg9X4")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6333773120"))

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 iPhone Trade Bot работает на Render!"

@web_app.route('/health')
def health():
    return "OK", 200

def run_web():
    web_app.run(host='0.0.0.0', port=8080)

print("🚀 iPhone Trade Bot запускается...")

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("📱 Каталог"), KeyboardButton("💰 Продать")],
        [KeyboardButton("🆘 Помощь"), KeyboardButton("📞 Контакты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 *Добро пожаловать в iPhone Trade Bot!*\n\nВыберите действие:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def catalog(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📱 *В продаже:*\n\n• iPhone 13 Pro - 65 000₽\n• iPhone 12 - 45 000₽",
        parse_mode='Markdown'
    )

async def sell(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💰 *Продать iPhone:*\n\n1. Отправьте фото\n2. Укажите модель и цену",
        parse_mode='Markdown'
    )

async def help_cmd(update: Update, context: CallbackContext):
    await update.message.reply_text("🆘 Помощь: пишите вопросы!")

async def contacts(update: Update, context: CallbackContext):
    await update.message.reply_text("📞 Контакты: @ваш_канал")

async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == "📱 Каталог":
        await catalog(update, context)
    elif text == "💰 Продать":
        await sell(update, context)
    elif text == "🆘 Помощь":
        await help_cmd(update, context)
    elif text == "📞 Контакты":
        await contacts(update, context)

async def handle_photo(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"✅ Фото получено от @{user.username}!")

def run_bot():
    print("🤖 Запускаю Telegram бота...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Telegram бот запущен!")
    app.run_polling()

if name == "__main__":
    web_thread = Thread(target=run_web, daemon=True)
    web_thread.start()
    import time
    time.sleep(2)
    run_bot()
