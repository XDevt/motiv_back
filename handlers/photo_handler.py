from core import router, types, F, bot
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from database import db


@router.message(F.photo)
async def photo_handler(message: types.Message):

    status = await db.get_status(message.from_user.id)

    if "AddNewTask" in status:
        quest_id = await db.create_unique_id()
        tittle = status.split("|&&&|")[1]
        cost = int(float(status.split("|&&&|")[2]))
        description = status.split("|&&&|")[3]
        btnTittle = status.split("|&&&|")[4]
        url = status.split("|&&&|")[5]
        chat_id = int(status.split("|&&&|")[6])
        maxMembers = int(status.split("|&&&|")[7])

        file_info = await bot.get_file(message.photo[-1].file_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, f"webapp/public/{quest_id}.png")

        await db.add_quest(quest_id, tittle, cost, description, btnTittle, url, chat_id, maxMembers)

        keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Включить сейчас")],
            [KeyboardButton(text="Включить позже")],
            [KeyboardButton(text="Отмена")]
        ], resize_keyboard=True)
        await message.answer("Task успешно создан! Включить сейчас?", reply_markup=keyboard)
        await db.set_status(message.from_user.id, f"TurnOnOff:{quest_id}")