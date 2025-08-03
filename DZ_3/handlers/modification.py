from aiogram import Router, types, F
from aiogram.filters import command, CommandObject

from DZ_3.repo import BookRepo, UserStatsRepo


modification_router = Router()

@modification_router.message(command.Command('add_book'))
async def add_book(message: types.Message):

    args = message.text.split()[1:]
    user_id = message.from_user.id

    if not args or len(args) != 2:
        await message.answer("Oops! Usage: /add_book 'title' 'pages_count'")
        return

    title, pages_count = args
    await BookRepo("database.db").create_book(user_id, title, pages_count)
    await UserStatsRepo("database.db").update_stats(user_id)

    await message.answer(f'Mission completed! Book add!')


@modification_router.message(command.Command('remove_book'))
async def remove_book(message: types.Message):
    args = message.text.split()[1:]
    user_id = message.from_user.id

    if not args or len(args) != 1:
        await message.answer(r"Oops! </remove_book 'book_id'>")
        return

    await BookRepo("database.db").delete_book(user_id, *args)
    await UserStatsRepo("database.db").update_stats(user_id)

    await message.answer(f'Mission completed! Book delete!')