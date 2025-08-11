from __future__ import annotations

import aiosqlite

from models import Book

class BookRepo:


    def __init__(self, db_path: str) -> None:
        self.db_path = db_path


    async def init_tables(self) -> None:

        sql_command = """
                        CREATE TABLE IF NOT EXISTS `Books` (
                            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                            `user_id` INTEGER NOT NULL,
                            `title` TEXT NOT NULL UNIQUE,
                            `pages_read` INTEGER DEFAULT 0 NOT NULL,
                            `pages_count` INTEGER NOT NULL,
                            `created_at` TEXT DEFAULT current_timestamp
                        );
                        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command)
            await db.commit()


    async def create_book(self, user_id: int, title: str, pages_count: int) -> Book:

        sql_command = f"""
                        INSERT INTO `Books` (`user_id`, `title`, `pages_count`) VALUES (
                            ?, ?, ?
                        )
                        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [user_id, title, pages_count])
            await db.commit()

            cursor = await db.execute(
                "SELECT * FROM `Books` WHERE `title` = ?", [title]
            )

            raw_book = await cursor.fetchone()
            return Book(**dict(raw_book))

    async def update_pages(self, user_id: int, book_id: int, pages: int) -> Book:

        sql_command = """
                        UPDATE `Books`
                        SET `pages_read` = ?
                        WHERE `id`=? AND `user_id` = ?;
                        """

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [pages, book_id, user_id])
            await db.commit()

            cursor = await db.execute(
                "SELECT * FROM `Books` WHERE `id` = ?", [book_id]
            )

            raw_book = await cursor.fetchone()
            return Book(**dict(raw_book))

    async def fetch_books(self, user_id: int):

        sql_command = """
                        SELECT `id`, `title`, `pages_read`, `pages_count` FROM `Books`
                        WHERE `user_id` = ?;
                        """

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command,[user_id])

            all_books = await cursor.fetchall()
            return all_books


    async def delete_book(self, user_id: int, book_id: int) -> None:

        sql_command = """
                        DELETE FROM Books
                        WHERE id = ? AND user_id = ?;
                        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [book_id, user_id])
            await db.commit()



class UserStatsRepo:


    def __init__(self, db_path: str) -> None:
        self.db_path = db_path


    async def init_tables(self) -> None:
        sql_command = """
                        CREATE TABLE IF NOT EXISTS `UserStats` (
                            `user_id` INTEGER NOT NULL UNIQUE,
                            `total_books` INTEGER DEFAULT 0,
                            `total_pages` INTEGER DEFAULT 0
                        );
                        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command)
            await db.commit()


    async def get_stats(self, user_id: int):

        sql_command = """
                        SELECT * FROM UserStats WHERE user_id = ?;
        """

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [user_id])

            stats = await cursor.fetchall()
            return stats


    async def create_stats(self, user_id: int):
        if not await self.get_stats(user_id):
            sql_command = f"""
                           INSERT INTO `UserStats` (`user_id`) VALUES (
                               ?
                           )
                           """

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(sql_command, [user_id])
                await db.commit()


    async def update_stats(self, user_id: int):

        sql_command = f"""
                        UPDATE `UserStats`
                            SET total_books = (SELECT COUNT(*) FROM Books WHERE user_id = ?),
                                total_pages = (SELECT SUM(pages_read) FROM Books WHERE user_id = ?)
                            WHERE user_id = ?;
                               """

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(sql_command, [user_id,user_id,user_id])
            await db.commit()

