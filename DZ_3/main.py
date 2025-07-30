import asyncio

from repo import BookRepo, UserStatsRepo

def print_books(books):
    for book in books:
        print(f'<<{book[0]}>> - {book[1]}/{book[2]} стр.')
def print_stat(stats):
    print(f"Вы читаете {stats[0][1]} книги, всего прочитано {stats[0][2]} страницы.")

async def main():
    book_repo = BookRepo("database.db")
    user_stats_repo = UserStatsRepo("database.db")
    await user_stats_repo.init_tables()
    await book_repo.init_tables()





    #await book_repo.update_pages(3,5,2)
    books = await book_repo.fetch_books(user_id=1)
    print_books(books)


    await user_stats_repo.update_stats(1)
    print_stat(await user_stats_repo.get_stats(1))

    #await book_repo.delete_book(1, 3)

    '''books1 = await book_repo.fetch_books(user_id=1)
    print(books1)'''
asyncio.run(main())
