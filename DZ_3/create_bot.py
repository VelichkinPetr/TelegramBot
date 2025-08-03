import os, dotenv

from aiogram import Bot, Dispatcher


dotenv.load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()