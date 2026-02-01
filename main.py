import os
import logging
from telegram.ext import Application, CommandHandler

print("=" * 50)
print("🚀 iPhone Bot запускается...")
print("=" * 50)

TOKEN = os.getenv("TOKEN", "8525467586:AAFAmrbV-HMV36NOwOLLU3zKrT_UwnSg9X4")

async def start(update, context):
    await update.message.reply_text("🤖 Привет! Я бот для iPhone.")

def main():
    logging.basicConfig(level=logging.INFO)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ Telegram бот запущен!")
    app.run_polling()

if name == "__main__":
    main()
