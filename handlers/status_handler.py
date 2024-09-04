from core import router, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from database import db
from handlers.start_handler import start_handler


@router.message(F.text)
async def status_handler(message: types.Message):
    if await db.get_user(message.from_user.id) == None:
        return await start_handler(message)
    status = await db.get_status(message.from_user.id)

    if status != None:
        if "TurnOnOff" in status:
            quest_id = status.split(":")[1]

            if message.text == "Включить сейчас":
                await db.turn_on_quest(quest_id)
                await message.answer("Готово, task включен!", reply_markup=ReplyKeyboardRemove())
                await db.set_status(message.from_user.id)

            elif message.text == "Включить позже":
                await message.answer("Хорошо, task выключен!", reply_markup=ReplyKeyboardRemove())
                await db.set_status(message.from_user.id)

            elif message.text == "Отмена":
                await db.delete_quest(quest_id)
                await message.answer("Task удален!", reply_markup=ReplyKeyboardRemove())
                await db.set_status(message.from_user.id)

            else:
                keyboard = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text="Включить сейчас")],
                    [KeyboardButton(text="Включить позже")],
                    [KeyboardButton(text="Отмена")]
                ], resize_keyboard=True)
                await message.answer("Воспользуйтесь клавиатурой ниже 👇", reply_markup=keyboard)