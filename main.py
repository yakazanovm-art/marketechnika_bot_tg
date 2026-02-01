import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from threading import Thread
from flask import Flask

# ====== КОНФИГУРАЦИЯ ======
TOKEN = os.getenv("TOKEN", "8525467586:AAFAmrbV-HMV36NOwOLLU3zKrT_UwnSg9X4")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6333773120"))

# Веб-сервер для Render (обязательно!)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 iPhone Trade Bot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                max-width: 600px;
                width: 90%;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .status {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            a {
                color: #4adeff;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
            .btn {
                display: inline-block;
                background: #4adeff;
                color: #000;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 10px;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 iPhone Trade Bot</h1>
            <div class="status">
                <p>✅ <strong>Бот активен и работает на Render!</strong></p>
                <p>🕒 Сервер работает 24/7</p>
                <p>📱 Telegram бот готов к работе</p>
            </div>
            <p>Этот веб-сервер поддерживает работу Telegram бота</p>
            <p>Бот автоматически перезапускается при сбоях</p>
            <div style="margin-top: 30px;">
                <a href="https://t.me/your_bot_username" class="btn">🔗 Перейти в бота</a>
                <a href="https://render.com/docs" class="btn">📚 Документация Render</a>
            </div>
        </div>
    </body>
    </html>
    """

@web_app.route('/health')
def health():
    return "OK", 200

def run_web():
    web_app.run(host='0.0.0.0', port=8080)

# ====== ТЕЛЕГРАМ БОТ ======
print("🚀 iPhone Trade Bot запускается на Render...")

async def start(update: Update, context: CallbackContext):
    """Главное меню"""
    keyboard = [
        [KeyboardButton("📱 Каталог"), KeyboardButton("💰 Продать")],
        [KeyboardButton("🆘 Помощь"), KeyboardButton("📞 Контакты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 *Добро пожаловать в iPhone Trade Bot!*\n\n"
        "📍 *Работаем на Render.com 24/7*\n\n"
        "✨ *Что можно сделать:*\n"
        "• 📱 Смотреть каталог iPhone\n"
        "• 💰 Продать свой iPhone\n"
        "• 📞 Связаться с менеджером\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def catalog(update: Update, context: CallbackContext):
    """Каталог"""
    catalog_text = """
📱 *Каталог iPhone:*

*1. iPhone 13 Pro 256GB*
💾 Память: 256 ГБ
🎨 Цвет: Синий
⭐ Состояние: Отличное
💰 Цена: *65 000₽*
📝 Батарея 92%, полная комплектация

*2. iPhone 12 128GB*
💾 Память: 128 ГБ
🎨 Цвет: Черный
⭐ Состояние: Хорошее
💰 Цена: *45 000₽*
📝 Мелкие царапины

*3. iPhone 14 Pro Max 512GB*
💾 Память: 512 ГБ
🎨 Цвет: Фиолетовый
⭐ Состояние: Идеальное
💰 Цена: *85 000₽*
📝 Гарантия до 2025 года

💬 *Для покупки напишите нам!*
"""
    await update.message.reply_text(catalog_text, parse_mode='Markdown')

async def sell(update: Update, context: CallbackContext):
    """Продажа"""
    await update.message.reply_text(
        "💰 *Продать свой iPhone:*\n\n"
        "Отправьте:\n"
        "1. 📸 Фотографии (2-5 шт)\n"
        "2. 📱 Модель и память\n"
        "3. ⭐ Состояние\n"
        "4. 💰 Желаемую цену\n\n"
        "*Пример сообщения:*\n"
        "iPhone 13 Pro, 256GB, отличное состояние, 60000₽",
        parse_mode='Markdown'
    )

async def help_cmd(update: Update, context: CallbackContext):
    """Помощь"""
    help_text = """
🆘 *Помощь по боту:*

*Для покупателей:*
1. Нажмите '📱 Каталог'
2. Выберите модель
3. Напишите нам для покупки

*Для продавцов:*
1. Нажмите '💰 Продать'
2. Отправьте фото iPhone
3. Опишите состояние
4. Укажите цену

*Команды:*
/start - Главное меню
/catalog - Каталог
/help - Эта справка

⏱ *Время ответа:* 5-15 минут
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def contacts(update: Update, context: CallbackContext):
    """Контакты"""
    contacts_text = """
📞 *Наши контакты:*

*Telegram канал:* @ваш_канал
*Телефон:* +7 (XXX) XXX-XX-XX
*Email:* iphone@example.com

*Режим работы:*
Пн-Пт: 10:00-20:00
Сб-Вс: 11:00-18:00

📍 Москва, встреча по записи
"""
    await update.message.reply_text(contacts_text, parse_mode='Markdown')

async def handle_text(update: Update, context: CallbackContext):
    """Обработка текста"""
    text = update.message.text
    
    if text == "📱 Каталог":
        await catalog(update, context)
    elif text == "💰 Продать":
        await sell(update, context)
    elif text == "🆘 Помощь":
        await help_cmd(update, context)
    elif text == "📞 Контакты":
        await contacts(update, context)
    else:
        await update.message.reply_text("Используйте кнопки меню! 😊")

async def handle_photo(update: Update, context: CallbackContext):
    """Обработка фото"""
    user = update.effective_user
    await update.message.reply_text(
        f"✅ *Фото получено!*\n\n"
        f"Спасибо, @{user.username}!\n"
        f"Теперь опишите ваш iPhone:\n\n"
        f"1. Модель\n"
        f"2. Память\n"
        f"3. Состояние\n"
        f"4. Цена\n\n"
        f"*Пример:* iPhone 13 Pro, 256GB, отличное, 60000₽",
        parse_mode='Markdown'
    )

def run_bot():
    """Запуск Telegram бота"""
    print("🤖 Запускаю Telegram бота...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("✅ Telegram бот запущен!")
    print("🌐 Веб-сервер работает на порту 8080")
    
    app.run_polling()

if name == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    web_thread = Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Даем время веб-серверу запуститься
    import time
    time.sleep(2)
    
    # Запускаем бота
    run_bot()
