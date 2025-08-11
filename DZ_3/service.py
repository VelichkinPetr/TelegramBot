from __future__ import annotations

from repo import BookRepo, UserStatsRepo


class BookService:

    def check_element(self, element, list_of_lists):
        '''
        Проверка, есть ли значение в матрице.

        :param element: искомый элемент
        :param list_of_lists: область поиска (матрица)
        :return: bool
        '''

        for sublist in list_of_lists:
            if element in sublist:
                return True
        return False

    def search_element(self, elem, list_of_lists):
        '''
        Поиск значения в матрице

        :param elem: искомый элемент
        :param list_of_lists: область поиска (матрица)
        :return: строка матрицы or None
        '''
        for sublist in list_of_lists:
            if sublist[0] == elem:
                return sublist
        return None

    async def add_book(self, user_id: int, args) -> None:

        '''
        :param user_id: int
        :param args: title: str, pages_count: int
        :return: None
        '''

        if not args or len(args) < 2:
            raise ValueError

        if not args[-1].isdigit():
            raise TypeError

        title = " ".join(args[:-1])
        pages_count = args[-1]

        if self.check_element(title, await self.list_books(user_id)):
            raise KeyError

        await BookRepo("database.db").create_book(user_id, title, pages_count)
        await UserStatsRepo("database.db").update_stats(user_id)

    async def increase_read_pages(self, user_id: int, args) -> None:

        '''
        :param user_id: int
        :param args: book_id: int, pages: int
        :return: None
        '''

        if not args or len(args) != 2:
            raise ValueError

        if not args[0].isdigit():
            print(args)
            raise TypeError

        if not args[1].isdigit():
            raise IndexError

        book_id, page = args
        list_books = await self.list_books(user_id)

        if not self.check_element(int(book_id), list_books):
            raise KeyError

        book = self.search_element(int(book_id), list_books)
        if book is None or book[3] < int(page):
            raise AttributeError

        await BookRepo("database.db").update_pages(user_id, int(book_id), int(page))
        await UserStatsRepo("database.db").update_stats(user_id)

    async def list_books(self, user_id: int) -> list:

        '''
        :param user_id: int
        :return: list
        '''
        return list(await BookRepo("database.db").fetch_books(user_id))

    async def remove_book(self, user_id: int, args) -> None:

        '''
        :param user_id: int
        :param args: book_id: int
        :return: None
        '''

        if not args or len(args) != 1:
            raise ValueError

        if not args[0].isdigit():
            raise TypeError

        book_id, = args
        list_books = await self.list_books(user_id)

        if not self.check_element(int(book_id), list_books):
            raise KeyError

        await BookRepo("database.db").delete_book(user_id, int(book_id))
        await UserStatsRepo("database.db").update_stats(user_id)