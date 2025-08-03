from aiogram import Router,types
from aiogram.filters import command

from DZ_3.repo import BookRepo, UserStatsRepo


start_router = Router()

@start_router.message(command.CommandStart())
async def start(message: types.Message):

    book_repo = BookRepo("database.db")
    user_stats_repo = UserStatsRepo("database.db")

    await user_stats_repo.init_tables()
    await user_stats_repo.create_stats(message.from_user.id)

    await book_repo.init_tables()
    await message.answer(f'Hello {list(await book_repo.fetch_books(user_id=message.from_user.id))}')
