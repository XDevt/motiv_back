from database.configuration import *

async def create_unique_id():
    return randint(1, 10000000000)

def get_date_now(t=TIME_FORMAT):
    return datetime.now().strftime(t)


def get_date_from_timestamp(timestamp, t=TIME_FORMAT):
    return datetime.fromtimestamp(timestamp).strftime(t)


def get_timestamp(date, t=TIME_FORMAT):
    return datetime.strptime(date, t).timestamp()


def get_next_date(year=None, month=None, days=None, hours=None, minutes=None, seconds=None, t='%Y-%m-%d %H:%M:%S'):
    now = datetime.now()

    if year != None: next_date = now + relativedelta(years=1)
    if month != None: next_date = now + timedelta(days=calendar.monthrange(date.today().year, date.today().month)[1])
    if days != None: next_date = now + timedelta(days=days)
    if hours != None: next_date = now + timedelta(hours=hours)
    if minutes != None: next_date = now + timedelta(minutes=minutes)
    if seconds != None: next_date = now + timedelta(seconds=seconds)

    return next_date.strftime(t)


def get_strptime(date, t=TIME_FORMAT):
    return datetime.strptime(date, t)

async def add_user(user_id, first_name, username):
    conn = get_conection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users VALUES(?,?,?,?,?,?,?)", (user_id, None, first_name, username, 0, 0, 0))
    conn.commit()
    conn.close()

async def get_user(user_id):
    conn =get_conection()
    cur = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_conection()
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users

async def get_status(user_id):
    user = await get_user(user_id)
    return user['status']

async def set_status(user_id, new_status=None):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE users
SET status = ?
WHERE user_id = ?    
"""
    cur.execute(sql, (new_status, user_id))
    conn.commit()
    conn.close()

async def add_quest(quest_id, tittle, cost, description, btnTittle, url, chat_id, maxMembers):
    conn = get_conection()
    cur = conn.cursor()
    channel = json.dumps({'url': f"{url}", "chat_id": chat_id})
    data = (
        quest_id,
        tittle,
        str(quest_id),
        cost,
        description,
        btnTittle,
        channel,
        maxMembers,
        0,
        0
    )
    cur.execute("INSERT INTO quests VALUES(?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()

async def update_quest_now_members(quest_id, new_count):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE quests
SET nowMembers = ?
WHERE quest_id = ?
    """
    cur.execute(sql, (new_count, quest_id))
    conn.commit()
    conn.close()

async def turn_on_quest(quest_id):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE quests
SET status = ?
WHERE quest_id = ?
    """
    cur.execute(sql, (1, quest_id))
    conn.commit()
    conn.close()

async def turn_off_quest(quest_id):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE quests
SET status = ?
WHERE quest_id = ?
    """
    cur.execute(sql, (0 , quest_id))
    conn.commit()
    conn.close()

async def delete_quest(quest_id):
    conn = get_conection()
    cur = conn.cursor()
    cur.execute("DELETE FROM quests WHERE quest_id = ?", (quest_id,))
    conn.commit()
    conn.close()

async def update_quest_now_participants(quest_id, new_count):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE quests
SET nowMembers = ?
WHERE quest_id = ?
    """
    cur.execute(sql, (new_count, quest_id))
    conn.commit()
    conn.close()

async def get_all_not_completed_quest(user_id):
    quests = await get_active_quests()
    tasks = []
    for quest in quests:
        completed_quest = await get_completed_quest(user_id, quest['quest_id'])
        if completed_quest == None and quest["status"] == 1:
            url = await get_quest_button_urls(quest['quest_id'])
            tasks.append({
                "id": quest['quest_id'],
                "title": quest['tittle'],
                "description": quest["image"],
                "img": quest["description"],
                "cost": quest['cost'],
                "btnTitle": quest['btnTittle'],
                "link": f"{url}",
                "color": "DD3A64",
            })
    return tasks

async def get_completed_quests(user_id):
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM completed_quests WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return quests



async def get_completed_quest(user_id, quest_id):
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM completed_quests WHERE user_id = ? AND quest_id = ?", (user_id, quest_id)).fetchone()
    conn.close()
    return quests

async def get_all_quests():
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM quests").fetchall()
    conn.close()
    return quests

async def get_active_quests():
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM quests WHERE status = ?", (0,)).fetchall()
    conn.close()
    return quests

async def get_work_quests():
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM quests WHERE status = ?", (0,)).fetchall()
    conn.close()
    return quests

async def get_active_users_quests(user_id):
    quests = []
    all_quests = await get_work_quests()
    for quest in all_quests:
        if await get_completed_quest(user_id, quest['quest_id']) == None:
            quests.append(quest)
    return quests

async def get_quest(quest_id):
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM quests WHERE quest_id = ?", (quest_id, )).fetchone()
    conn.close()
    return quests

async def get_quest_now_participants(quest_id):
    quest = await get_quest(quest_id)
    return quest['nowMembers']

async def get_all_participants(quest_id):
    conn = get_conection()
    cur = conn.cursor()
    quests = cur.execute("SELECT * FROM completed_quests WHERE quest_id = ?", (quest_id,)).fetchall()
    conn.close()
    return quests

async def get_quest_button_urls(quest_id):
    quest = await get_quest(quest_id)
    return json.loads(quest['resource_url'])['url']

async def get_quest_button_chat_id(quest_id):
    quest = await get_quest(quest_id)
    return json.loads(quest['resource_url'])['chat_id']

async def add_completed_quest(user_id, quest_id):
    conn = get_conection()
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_quests VALUES(?,?)", (user_id, quest_id))
    conn.commit()
    conn.close()

async def delete_completed_quest(user_id, quest_id):
    conn = get_conection()
    cur = conn.cursor()
    cur.execute("DELETE FROM completed_quests WHERE user_id = ? AND quest_id = ?", (user_id, quest_id))
    conn.commit()
    conn.close()

async def get_user_balance(user_id):
    user = await get_user(user_id)
    return user['balance']

async def set_user_balance(user_id, new_balance):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE users
SET balance = ?
WHERE user_id = ?
"""
    cur.execute(sql, (new_balance, user_id))
    conn.commit()
    conn.close()

async def set_user_total_earn(user_id, new_total_earn):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE users
SET totalEarn = ?
WHERE user_id = ?
"""
    cur.execute(sql, (new_total_earn, user_id))
    conn.commit()
    conn.close()

async def set_user_task_complete(user_id, new_total_earn):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE users
SET taskComplete = ?
WHERE user_id = ?
"""
    cur.execute(sql, (new_total_earn, user_id))
    conn.commit()
    conn.close()

async def get_all_user_referrals(user_id):
    conn = get_conection()
    cur = conn.cursor()
    referrals = cur.execute("SELECT * FROM referrals WHERE referral_id = ?", (user_id,)).fetchall()
    conn.commit()
    return referrals

async def get_all_reff_data(user_id):
    reff_data = []
    referrals = await get_all_user_referrals(user_id)
    for referral in referrals:
        reff_data.append({
                    "tgid": referral["referrer_id"],
                    "avatar": f"/{referral["referrer_id"]}.jpg",
                    "income": referral["income"],
                    "name": referral["refName"],
                })


async def get_user_referer(user_id):
    conn = get_conection()
    cursor = conn.cursor()
    referer = cursor.execute(f"SELECT * FROM referrals WHERE referrer_id = ?", (user_id,)).fetchone()
    conn.close()
    return referer['referral_id'] if referer != None else None

async def add_new_referral(referal_id, referer_id, refName):
    conn = get_conection()
    cursor = conn.cursor()
    data = (
        referal_id,
        referer_id,
        0,
        refName
    )
    cursor.execute("INSERT INTO referrals VALUES (?,?,?,?)", data)
    conn.commit()
    conn.close()

async def get_user_referral_income(referral_id, referrer_id):
    conn = get_conection()
    cur = conn.cursor()
    income = cur.execute("SELECT * FROM referrals WHERE referral_id = ? AND referrer_id = ?", (referral_id, referrer_id)).fetchone()
    conn.close()
    return income["income"]

async def update_user_referral_income(referral_id, referrer_id, new_income):
    conn = get_conection()
    cur = conn.cursor()
    sql = """
UPDATE referrals
SET income = ?
WHERE referral_id = ? AND referrer_id = ? 
"""
    cur.execute(sql, (new_income, referral_id, referrer_id))