from aiogram import Router, types, F
from aiogram.filters import command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from DZ_3.service import BookService

modification_router = Router()


@modification_router.message(command.Command('add_book','a'))
async def add_book(message: types.Message):

    args = message.text.split()[1:]
    user_id = message.from_user.id

    try:
        await BookService().add_book(user_id, args)
        await message.answer(f'Mission completed! Book add!')

    except ValueError:
        await message.answer("Oops! Usage: /add_book of /a 'title' 'pages_count'")

    except TypeError:
        await message.answer("Oops! need is digit => 'pages_count'")

    except KeyError:
        await message.answer("Sorry Book in Base =)")


@modification_router.callback_query(F.data.startswith("r"))
async def remove_callback_handler(callback: types.CallbackQuery):

    args = callback.data.split()[1]
    user_id = callback.from_user.id

    await BookService().remove_book(user_id, args)
    await callback.message.answer(f'Mission completed! Book delete!')


@modification_router.message(command.Command('remove_book','r'))
async def remove_book(message: types.Message):

    args = message.text.split()[1:]
    user_id = message.from_user.id

    try:
        await BookService().remove_book(user_id, args)
        await message.answer(f'Mission completed! Book delete!')

    except ValueError:
        await message.answer(r"Oops! </remove_book or /r 'book_id'>")

    except TypeError:
        await message.answer("Oops! need is digit => 'book_id'")

    except KeyError:
        await message.answer("Sorry Book NOT in Base =(")


@modification_router.message(command.Command('list_books','l'))
async def list_books(message: types.Message):

    user_id = message.from_user.id
    list_books = await BookService().list_books(user_id)

    if len(list_books) == 0:
        return await message.answer('Book not found!')

    inl_kb_builder = InlineKeyboardBuilder()
    inl_btn_remove = InlineKeyboardButton(text='Удалить', callback_data=f"r {list_books[0][0]}")
    inl_kb_builder.add(inl_btn_remove)

    books = ''

    for i, book in enumerate(list_books):
        books += ''.join(f"{i+1}. '{book[1]}({book[0]})' - {book[2]}/{book[3]} стр.\n")

    await message.answer(books, reply_markup=inl_kb_builder.as_markup())


@modification_router.message(command.Command('mark_read','m'))
async def mark_read(message: types.Message):

    args = message.text.split()[1:]
    user_id = message.from_user.id

    try:
        await BookService().increase_read_pages(user_id, args)
        await list_books(message)
        await message.answer(f'Mission completed! Book update!')

    except ValueError:
        await message.answer(r"Oops! < /mark_read or /m 'book_id' 'page' >")

    except TypeError:
        await message.answer("Oops! need is digit  =>  'book_id'")

    except IndexError:
        await message.answer("Oops! need is digit  =>  'page'")

    except KeyError:
        await message.answer("Sorry Book NOT in Base =(")

    except AttributeError:
        await message.answer("Oops! 'page'  =>  pages count book")