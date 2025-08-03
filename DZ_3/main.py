import asyncio

from aiogram import types
from aiogram.filters import command
from repo import BookRepo, UserStatsRepo

from create_bot import bot, dp
from handlers.start import start_router
from handlers.modification import modification_router



async def main():

    dp.include_routers(start_router, modification_router)
    await dp.start_polling(bot)








    '''#await book_repo.update_pages(3,5,2)
    books = await book_repo.fetch_books(user_id=1)
    print_books(books)


    await user_stats_repo.update_stats(1)
    print_stat(await user_stats_repo.get_stats(1))

    #await book_repo.delete_book(1, 3)

    books1 = await book_repo.fetch_books(user_id=1)
    print(books1)'''

if __name__ == '__main__':
    asyncio.run(main())