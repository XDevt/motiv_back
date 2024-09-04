from core import Command, router, types, InlineKeyboardMarkup, InlineKeyboardButton, bot
from database import db


@router.message(Command('start'))
async def start_handler(message: types.Message):

    if await db.get_user(message.from_user.id) == None:
        user_profile_photos = await bot.get_user_profile_photos(message.from_user.id)

        if user_profile_photos.total_count > 0:
            photo = user_profile_photos.photos[0][-1]
            file_info = await bot.get_file(photo.file_id)
            file_path = file_info.file_path
            await bot.download_file(file_path, f"webapp/public/{message.from_user.id}.jpg")

    if " " in message.text:
        type = message.text.split(' ')[1].split('-')[0]
        if type == 'ref':
            data = message.text.split(' ')[1].split('-')[1]
            user = await db.get_user(message.from_user.id)
            if user == None and int(data) != message.from_user.id:
                await db.add_new_referral(data, message.from_user.id, message.from_user.first_name)
    await db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)

    web_app_url = 'https://motiv.pycuk.ru'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Open Web App", web_app=types.WebAppInfo(url=web_app_url))]
    ])
    await message.answer(f"""
Приветствую, {message.from_user.first_name} 👋

Здесь вы можете заработать деньги, выполняя лёгкие задания. 

❗️<i>От вас <b>НЕ</b> требуется <b>НИКАКИХ</b> вложений, противозаконных действий, документов или других конфидециальных данных.</i> 

<b>Любой</b>, кто будет просить у вас что-то подобное от лица нашего сервиса – <b>мошенник</b>. 

У нас всё максимально <b>просто и прозрачно:</b> 

• выполнил задание —> • получил <b>₽</b> на баланс —> • вывел их на карту

Чтобы приступить, нажми «💸<b>Задания</b>» и выбери любое задание. 

Чтобы посмотреть текущий баланс или вывести деньги, нажми «👨‍💻<b>Личный кабинет</b>».
""", reply_markup=keyboard)