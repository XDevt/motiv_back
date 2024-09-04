from aiogram import types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

router = Router()

dp = Dispatcher()
dp.include_router(router)

scheduler = AsyncIOScheduler()