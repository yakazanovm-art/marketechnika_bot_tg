Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
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
...         f"✅ *Фото получено!*\n\n"
...         f"Спасибо, @{user.username}!\n"
...         f"Теперь опишите ваш iPhone:\n\n"
...         f"1. Модель\n"
...         f"2. Память\n"
...         f"3. Состояние\n"
...         f"4. Цена\n\n"
...         f"*Пример:* iPhone 13 Pro, 256GB, отличное, 60000₽",
...         parse_mode='Markdown'
...     )
... 
... def run_bot():
...     """Запуск Telegram бота"""
...     print("🤖 Запускаю Telegram бота...")
...     
...     app = Application.builder().token(TOKEN).build()
...     
...     app.add_handler(CommandHandler("start", start))
...     app.add_handler(CommandHandler("catalog", catalog))
...     app.add_handler(CommandHandler("help", help_cmd))
...     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
...     app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
...     
...     print("✅ Telegram бот запущен!")
...     print("🌐 Веб-сервер работает на порту 8080")
...     
...     app.run_polling()
... 
... if name == "__main__":
...     # Запускаем веб-сервер в отдельном потоке
...     web_thread = Thread(target=run_web, daemon=True)
...     web_thread.start()
...     
...     # Даем время веб-серверу запуститься
...     import time
...     time.sleep(2)
...     
...     # Запускаем бота
