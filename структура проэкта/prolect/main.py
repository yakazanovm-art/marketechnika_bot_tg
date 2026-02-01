import json
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

TOKEN = os.getenv("8525467586:AAFAmrbV-HMV36NOwOLLU3zKrT_UwnSg9X4")
ADMIN_ID = int(os.getenv("6333773120"))

bot = Bot(TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Доступные айфоны")],
        [KeyboardButton(text="💰 Продать айфон")]
    ],
    resize_keyboard=True
)

class SellForm(StatesGroup):
    model = State()
    memory = State()
    condition = State()
    price = State()
    photo = State()

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Привет! Выбери действие:", reply_markup=keyboard)

@dp.message(F.text == "📱 Доступные айфоны")
async def show_phones(message: Message):
    with open("phones.json") as f:
        phones = json.load(f)

    text = "📱 В наличии:\n\n"

    for p in phones:
        text += f"{p['model']} | {p['memory']} | {p['price']}\n"

    await message.answer(text)

@dp.message(F.text == "💰 Продать айфон")
async def sell_start(message: Message, state: FSMContext):
    await state.set_state(SellForm.model)
    await message.answer("Напиши модель айфона:")

@dp.message(SellForm.model)
async def model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(SellForm.memory)
    await message.answer("Память (например 128GB):")

@dp.message(SellForm.memory)
async def memory(message: Message, state: FSMContext):
    await state.update_data(memory=message.text)
    await state.set_state(SellForm.condition)
    await message.answer("Состояние:")

@dp.message(SellForm.condition)
async def condition(message: Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await state.set_state(SellForm.price)
    await message.answer("Желаемая цена:")

@dp.message(SellForm.price)
async def price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(SellForm.photo)
    await message.answer("Теперь пришли фото:")

@dp.message(SellForm.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    data = await state.get_data()

    caption = (
        f"🔥 Новая заявка\n\n"
        f"Модель: {data['model']}\n"
        f"Память: {data['memory']}\n"
        f"Состояние: {data['condition']}\n"
        f"Цена: {data['price']}\n"
        f"От: @{message.from_user.username}"
    )

    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=caption
    )

    await message.answer("✅ Заявка отправлена!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
