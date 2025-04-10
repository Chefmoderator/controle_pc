import os
from bot.State import BotState
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from bot.volume import (
    voleme_menu,
    get_volume_now,
    asking_for_change_volume,
    change_volume,
    turn_on_the_sound,
    turn_off_the_sound,
    #volume_back
)

router = Router()

MAIN_BUTTONS = ["🔊 Регулировка звука"]

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔊 Регулировка звука")]],
    resize_keyboard=True
)

command_handlers = {}

async def fsm_conflict_check(message: types.Message, state: FSMContext, conflict_buttons: list):
    if message.text not in conflict_buttons:
        return False
    current_state = await state.get_state()
    if not current_state:
        await state.set_state(BotState.neutral)
        return False
    if current_state in [BotState.neutral.state, BotState.confirmation_of_fsm_stop.state]:
        return False
    await state.update_data(pending_command=message.text)
    await state.set_state(BotState.confirmation_of_fsm_stop)
    await message.answer("⚠️ Ты уже выполняешь действие. Прервать и начать новое? Напиши 'да' или 'нет'.")
    return True

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(BotState.neutral)
    await message.answer("👋 Привет, выбери действие", reply_markup=main_keyboard)

@router.message(Command('back'))
async def back(message: types.Message, state: FSMContext):
    await state.set_state(BotState.neutral)
    await message.answer("👋 Привет, выбери действие", reply_markup=main_keyboard)

@router.message(F.text == "🔊 Регулировка звука")
async def request_volume_menu(message: types.Message, state: FSMContext):
    if await fsm_conflict_check(message, state, MAIN_BUTTONS):
        command_handlers["🔊 Регулировка звука"] = request_volume_menu
        return
    await state.set_state(BotState.neutral)
    await voleme_menu(message)
command_handlers["🔊 Регулировка звука"] = request_volume_menu

@router.message(F.text=="🔊 Узнать звук сейчас")
async def volume_now(message: types.Message, state: FSMContext):
    await get_volume_now(message,state)


@router.message(F.text == "🔉 Изменить уровень звука")
async def waiting_for_asking_for_change_volume(message: types.Message,state:FSMContext):
    await asking_for_change_volume(message,state)

@router.message(StateFilter(BotState.waiting_for_asking_for_change_volume))
async def processed_change_volume(message: types.Message,state:FSMContext):
    await change_volume(message, state)

@router.message(F.text=="🔊 Включить звук")
async def processed_turn_on_the_sound(message:types.Message, state:FSMContext):
    await turn_on_the_sound(message,state)

@router.message(F.text=="🔇 Выключить звук")
async def processed_turn_off_the_sound(message:types.Message, state:FSMContext):
    await turn_off_the_sound(message,state)
