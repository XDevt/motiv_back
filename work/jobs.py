from database import db


async def check_complete_quest(bot):
    quests = await db.get_work_quests()
    for quest in quests:
        del_users = 0
        chat_id = await db.get_quest_button_chat_id(quest['quest_id'])
        participants = await db.get_all_participants(quest['quest_id'])
        for participant in participants:
            user = await bot.get_chat_member(chat_id, participant['user_id'])
            if user.status not in ["member", "creator", "admin"]:
                await db.delete_completed_quest(participant['user_id'], quest['quest_id'])
                await db.set_user_balance(participant['user_id'], await db.get_user_balance(participant['user_id']) - quest['price'])
                del_users += 1
        if del_users != 0:
            now_participants = await db.get_quest_now_participants(quest['quest_id'])
            await db.update_quest_now_participants(quest['quest_id'], int(now_participants - del_users))