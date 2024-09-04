from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from core import bot
import config
from database import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/complete_quest', methods=['POST'])
async def check_complete_quest():
    try:
        data = request.json
        user_id = data.get('tg_user_id')
        quest_id = data.get('quest_id')
        quest = await db.get_quest(quest_id)
        user = await db.get_user(user_id)
        chat_id = await db.get_quest_button_chat_id(quest_id)
        chat_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if chat_status.status in ["member", "creator", "administrator"]:
            await db.set_user_balance(user_id, user['balance'] + quest["cost"])
            await db.set_user_total_earn(user_id, user['totalEarn'] + quest["cost"])
            await db.add_completed_quest(user_id=user_id, quest_id=quest_id)
            await db.set_user_task_complete(user_id, user["taskComplete"] + 1)
            await db.update_quest_now_members(quest_id, quest["nowMembers"] + 1)
            user_ref_id = await db.get_user_referer(user_id)
            if user_ref_id != None:
                user_ref = await db.get_user(user_ref_id)
                await db.set_user_balance(user_id, user_ref['balance'] + round((quest["cost"] * config.ref_percent) / 100, 2))
                await db.set_user_total_earn(user_id, user['totalEarn'] + round((quest["cost"] * config.ref_percent) / 100, 2))
                await db.update_user_referral_income(user_ref_id, user_ref, await db.get_user_referral_income(user_ref_id, user_ref) + round((quest["cost"] * config.ref_percent) / 100, 2))
            if quest["nowMembers"] + 1 == quest["maxMembers"]:
                await db.turn_off_quest(quest_id)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "failed"})
    except:
        return jsonify({"status": "failed"})


@app.route('/get_data_card', methods=['POST'])
async def get_data_card_number():
    try:
        data = request.json
        user_id = data.get('tg_user_id')
        card_number = data.get('card_number')
        balance = await db.get_user_balance(user_id)
        await db.set_user_balance(user_id, 0)
        await bot.send_message(config.admin_chat_id, f"""
<b>Новая заявка на вывод!</b>

<b>Сумма:</b> {balance}P
<b>Номер карты:</b> {card_number}
""")

        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "failed"})


@app.route('/get_data_ton', methods=['POST'])
async def get_data_ton_address():
    try:
        data = request.json
        user_id = data.get('tg_user_id')
        ton_address = data.get('ton_address')
        balance = await db.get_user_balance(user_id)
        await db.set_user_balance(user_id, 0)
        await bot.send_message(config.admin_chat_id, f"""
<b>Новая заявка на вывод!</b>

<b>Сумма:</b> {balance}P
<b>Номер кошелька:</b> {ton_address}
""")

        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "failed"})


@app.route('/get_user_data', methods=['POST'])
async def receive_data():
    try:
        data = request.json
        user_id = data.get('tg_user_id')
        user = await db.get_user(user_id)

        user_data = {
            "tgid": user_id,
            "balance": user['balance'],
            "totalEarn": user['totalEarn'],
            "tasksComplete": user['taskComplete'],
            "tasks": await db.get_all_not_completed_quest(user_id),
            "friends": await db.get_all_reff_data(user_id)
        }

        return jsonify({"status": "success", "user_data": user_data})
    except:
        return jsonify({"status": "failed"})