import os
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.filters.state import StateFilter  # Импортируем фильтр состояния
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from bot.State import BotState
from bot.handler import BotState

# Получаем доступ к управлению звуком
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Функция отображения меню громкости
async def voleme_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔊 Узнать звук сейчас"),KeyboardButton(text="🔉 Изменить уровень звука")],
            [KeyboardButton(text="🔊 Включить звук"), KeyboardButton(text="🔇 Выключить звук")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие с громкостью:", reply_markup=keyboard)
# Функция получения текущего уровня громкости

async def get_volume_now(message: types.Message, state: FSMContext):
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    current_volume = int(current_volume)
    await message.answer(f"🔊 Текущий уровень громкости: {current_volume}%")

# Функция для запроса на увеличение громкости
async def asking_for_change_volume(message: types.Message, state: FSMContext):
    await message.answer("🔊 Напишите какой уровень звука вам нужен ")
    await state.set_state(BotState.waiting_for_asking_for_change_volume)

# Обработчик для увеличения громкости
async def change_volume(message: types.Message, state: FSMContext):
    try:
        if message.text and int(message.text) < 101 and message.text.isdigit():
            new_volume = int(message.text) / 100
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            await message.answer(f"🔊 Уровень звука сейча: {new_volume * 100}%")
        else:
            await message.answer("❌ Ошибка! Введите число для увеличения громкости.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    finally:
        await state.clear()

#Функция для включения звука
async def turn_on_the_sound(message:types.Message, state:FSMContext):
    volume.SetMute(False,None)
    await message.answer("🔊 Звук включен")

#Функция для выключения звука
async def turn_off_the_sound(message:types.Message, state:FSMContext):
    volume.SetMute(True,None)
    await message.answer("🔇 Звук выключен")

#Функция для возвращения назад
# async def volume_back(message:types.Message,state:FSMContext):
#     await message.answer("Напишите комнаду /back , что бы вернуться в меню")