import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
from threading import Thread
import time

# ====== КОНФИГУРАЦИЯ ======
TOKEN = os.getenv("TOKEN", "8525467586:AAFAmrbV-HMV36NOwOLLU3zKrT_UwnSg9X4")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6333773120"))

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 iPhone Trade Bot запускается на Render...")
print("=" * 50)

# ====== FLASK ДЛЯ RENDER ======
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head><title>🤖 iPhone Bot</title></head>
        <body style="text-align: center; padding: 50px; background: #f0f0f0;">
            <h1>🤖 iPhone Trade Bot</h1>
            <p>✅ Бот работает на Render 24/7</p>
            <p>📱 Telegram бот активен</p>
            <p>🕒 Серверное время: """ + time.strftime('%H:%M:%S') + """</p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ====== ТЕЛЕГРАМ БОТ ======
async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    keyboard = [
        [KeyboardButton("📱 Каталог"), KeyboardButton("💰 Продать")],
        [KeyboardButton("🆘 Помощь"), KeyboardButton("📞 Контакты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 *Добро пожаловать в iPhone Trade Bot!*\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    print(f"✅ Пользователь {update.effective_user.username} запустил бота")

async def catalog(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📱 *Каталог:*\n\n• iPhone 13 Pro - 65 000₽\n• iPhone 12 - 45 000₽",
        parse_mode='Markdown'
    )

async def sell(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💰 *Продать iPhone:*\n\nОтправьте фото и описание",
        parse_mode='Markdown'
    )

async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == "📱 Каталог":
        await catalog(update, context)
    elif text == "💰 Продать":
        await sell(update, context)
    elif text == "🆘 Помощь":
        await update.message.reply_text("Помощь: @ваш_канал")
    elif text == "📞 Контакты":
        await update.message.reply_text("Контакты: +7 XXX XXX-XX-XX")

async def handle_photo(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(
        f"✅ Фото получено, @{user.username}!\nОпишите модель и цену.",
        parse_mode='Markdown'
    )

def run_telegram_bot():
    """Запуск Telegram бота"""
    print("🤖 Запускаю Telegram бота...")
    
    bot_app = Application.builder().token(TOKEN).build()
    
    # Обработчики
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    bot_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("✅ Telegram бот запущен!")
    print("🌐 Веб-сервер работает")
    
    bot_app.run_polling()

# ====== ГЛАВНЫЙ ЗАПУСК ======
if name == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Даем время Flask запуститься
    time.sleep(2)
    
    # Запускаем Telegram бота
    try:
        run_telegram_bot()
    except Exception as e:
        print(f"❌ Ошибка в боте: {e}")
        print("🔁 Перезапуск через 5 секунд...")
        time.sleep(5)
