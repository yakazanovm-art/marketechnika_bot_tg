import json
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("📱 Доступные айфоны")
keyboard.add("💰 Продать айфон")

class SellForm(StatesGroup):
    model = State()
    memory = State()
    condition = State()
    price = State()
    photo = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Выбери действие:", reply_markup=keyboard)

@dp.message_handler(text="📱 Доступные айфоны")
async def phones(message: types.Message):
    with open("phones.json") as f:
        phones = json.load(f)

    text = "📱 В наличии:\n\n"

    for p in phones:
        text += f"{p['model']} | {p['memory']} | {p['price']}\n"

    await message.answer(text)

@dp.message_handler(text="💰 Продать айфон")
async def sell(message: types.Message):
    await SellForm.model.set()
    await message.answer("Модель айфона:")

@dp.message_handler(state=SellForm.model)
async def model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await SellForm.memory.set()
    await message.answer("Память:")

@dp.message_handler(state=SellForm.memory)
async def memory(message: types.Message, state: FSMContext):
    await state.update_data(memory=message.text)
    await SellForm.condition.set()
    await message.answer("Состояние:")

@dp.message_handler(state=SellForm.condition)
async def condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await SellForm.price.set()
    await message.answer("Цена:")

@dp.message_handler(state=SellForm.price)
async def price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await SellForm.photo.set()
    await message.answer("Пришли фото:")

@dp.message_handler(content_types=types.ContentType.PHOTO, state=SellForm.photo)
async def photo(message: types.Message, state: FSMContext):
    data = await state.get_data()

    caption = f"""
🔥 Новая заявка

Модель: {data['model']}
Память: {data['memory']}
Состояние: {data['condition']}
Цена: {data['price']}
"""

    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)

    await message.answer("✅ Отправлено!")
    await state.finish()

if name == "__main__":
    executor.start_polling(dp)
