import asyncio

from repo import BookRepo


async def main():

    book_repo = BookRepo("database.db")
    book = await book_repo.create_book(user_id=1, title="Колобок", pages_count=20)
    print(book)




asyncio.run(main())
