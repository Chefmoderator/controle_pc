import asyncio , os
try:
    from aiogram import Router, types, F, Dispatcher
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.state import State, StatesGroup
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
    from aiogram.filters import Command
except:
    os.system("python -m pip install aiogram")
    from aiogram import Router, types, F, Dispatcher
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.state import State, StatesGroup
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
    from aiogram.filters import Command

router = Router()
@router.message(Command("start"))
async def head_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Регулировать звук")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберет действия:", reply_markup=keyboard)
