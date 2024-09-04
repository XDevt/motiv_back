import logging
from work import jobs
from work.app import app
from core import dp, bot, scheduler
import threading
from apscheduler.triggers.cron import CronTrigger
import asyncio

logging.basicConfig(level=logging.INFO)

async def run_bot():
    from handlers import router
    scheduler.add_job(jobs.check_complete_quest, CronTrigger(hour=0, minute=0), args=(bot,))
    scheduler.start()
    await dp.start_polling(bot)

def run_flask():
    app.run(host="0.0.0.0", port=5000, use_reloader=False)

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    start_bot()
    flask_thread.join()
