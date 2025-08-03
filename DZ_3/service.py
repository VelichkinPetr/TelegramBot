from models import Book


"""
CREATE TABLE Persons (
    name VARCHAR(128),
    age INTEGER
);
"""

"""
USE database;

UPDATE `Persons` SET `name` = 'Дмитрий'
WHERE `age` > 22;


INSERT INTO `Persons` VALUES
    ('Shaban', 17),
    ('Ivan', 20) 
;
    
DELETE FROM `Persons`
    WHERE (`Persons`.`age` = 18 OR `Persons`.`name` = 'Шабан');

"""

class BookService:

    async def add_book(self, user_id: int, title: str, pages_count: int) -> None:
        pass

    async def increase_read_pages(self, user_id: int, book_id: int, pages: int) -> None:
        pass

    async def list_books(self, user_id: int) -> list[Book]:
        pass

    async def remove_book(self, user_id: int, book_id: int) -> None:
        pass


class UserStatsService:
    pass