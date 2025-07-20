import asyncio

import aiogram
from aiogram import types
from aiogram.filters import command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import *


# Хранилище данных
class KinomanBotData:


    def __init__(self):
        self.favorites = {}
        self.movies_db = {
            'comedy': {
                2022: ['Чебурашка', 'Холоп 2', 'Ёлки 9'],
                2023: ['Не одна дома', 'Манюня']
            },
            'drama': {
                2022: ['1992', 'Сердце пармы'],
                2023: ['Праведник']
            },
            'action': {
                2022: ['Топ Ган: Мэверик', 'Джон Уик 4'],
                2023: ['Миссия невыполнима 7']
            }
        }

    def save_movie(self, user_id, movie_title):

        if user_id not in self.favorites:
            self.favorites[user_id] = []

        if movie_title not in self.favorites[user_id]:
            self.favorites[user_id].append(movie_title)
            return "Сохранено!"

        return "Фильм уже в избранном"

    def get_recommendation(self, genre, year):

        if genre in self.movies_db and year in self.movies_db[genre]:
            return self.movies_db[genre][year]

        return None

    def get_favorites(self, user_id):
        return self.favorites.get(user_id, [])

#Создание хранилища
bot_data = KinomanBotData()

#Создание бота
bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher()

iter_movies = None
current_movie = None

#Создание клавиатуры кнопок
def create_keyboard(list_name, bottons_in_row):

    kb_builder = ReplyKeyboardBuilder()

    for i in list_name:
        kb_builder.add(types.KeyboardButton(text= str(i)))
    kb_builder.adjust(bottons_in_row)

    return kb_builder.as_markup(resize_keyboard = True)


# Обработчик команды /start
@dp.message(command.CommandStart())
async def start_command(message: types.Message):

    REFERENCE = (
        "Привет! Я бот-киноман!\n\n"
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/recommend <жанр> <год> - получить рекомендацию\n"
        "/save <название фильма> - сохранить фильм\n"
        "/mylist - посмотреть избранные фильмы"
    )
    await message.answer(REFERENCE)

# Обработчик команды /mylist
@dp.message(command.Command(COMMAND_MYLIST))
async def mylist_command(message: types.Message):

    favorites = bot_data.get_favorites(message.from_user.id)
    if not favorites:
        await message.answer("Ваш список избранного пуст")
        return

    response = "Ваши избранные фильмы:\n"
    for i, movie in enumerate(favorites):
        response += f"{i+1}. {movie}\n"

    await message.answer(response)

#Обработчик команды /save
@dp.message(command.Command(COMMAND_SAVE))
async def save_command(message: types.Message, command: command.CommandObject):

    args = command.args
    if not args:
        await message.answer("Укажите название фильма после команды")
        return

    response = bot_data.save_movie(message.from_user.id, args)
    await message.answer(response)

#Обработчик кнопки СОХРАНИТЬ
@dp.message(F.text.lower() == BOTTON_SAVE)
async def save_botton_command(message: types.Message):

    response = bot_data.save_movie(message.from_user.id, current_movie)
    await message.answer(response)

#Обработчик кнопки СЛЕДУЮЩИЙ
@dp.message(F.text.lower() == BOTTON_NEXT)
async def next_command(message: types.Message):

    global iter_movies,current_movie

    try:
        current_movie = iter_movies.__next__()
        await message.answer(current_movie)
    except StopIteration:
        await message.answer(f'Мне больше нечего предложить :( ',
                             reply_markup=types.ReplyKeyboardRemove())

#Обработчик команды /recommend
@dp.message(command.Command(COMMAND_RECOMMEND))
async def recommendation_film(message: types.Message, command: command.CommandObject):

    args = command.args
    if args is None:
        await message.answer("Используйте формат: /recommend <жанр> <год>")
        return

    args = list (map(lambda elem: int(elem) if elem.isdigit() else elem,args.split(' ')))
    find_movies = bot_data.get_recommendation(*args)

    if find_movies is None:
        await message.reply(f"Таких фильмов нет ((")
        return

    global current_movie,iter_movies
    iter_movies = find_movies.__iter__()
    current_movie = iter_movies.__next__()
    await message.answer(current_movie, reply_markup=create_keyboard(["Сохранить", "Следующий"], 2))


async def main():
    print("Бот просыпайся")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())