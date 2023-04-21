import random
from config import API_TOKEN
from texts import FLIRT, COMPLIMENTS, STIKERS_BOMZH, QUIZ, HELP_CMD
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# Ведение журнала
logging.basicConfig(level=logging.INFO)

# Ициницализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Список названий всех фотографий из директории images
files_img = os.listdir('images/')


# Основная клавиатура бота
def main_menu() -> types.ReplyKeyboardMarkup:
    main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Флирт с джентельменом 🤭')
    button2 = types.KeyboardButton('Получить комплимент 😍')
    button3 = types.KeyboardButton('Покажи фотку')
    button4 = types.KeyboardButton('Викторина')
    main_kb.add(button1, button2).add(button3, button4)
    return main_kb


# Временное хранилище текущего статуса викторины
results = dict()


# ВСЕ КОМАНДЫ И MESSAGE_HANDLERS
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    '''
    Обработчик команды /start
    '''
    await message.reply(text=HELP_CMD,
                        reply_markup=main_menu(),
                        parse_mode="HTML")


@dp.message_handler(Text('Главное меню'))
async def get_main_menu(message: types.Message):
    await message.reply(text='Викторина окончена.', reply_markup=main_menu())


@dp.message_handler(Text('Покажи фотку'))
async def send_img(message: types.Message):
    # Выбор рандомной фотки из папки images
    rand_img = random.choice(files_img)
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=types.InputFile(f'images/{rand_img}'))


@dp.message_handler(Text('Флирт с джентельменом 🤭'))
async def send_flirt(message: types.Message):
    # Рандомный флирт из texts.py
    rand_fl = random.choice(FLIRT)
    await message.answer(rand_fl)

    # Рандомный стикер из texts.py
    rand_stick = random.choice(STIKERS_BOMZH)
    await bot.send_sticker(message.from_user.id, sticker=rand_stick)


@dp.message_handler(Text('Получить комплимент 😍'))
async def send_compliment(message: types.Message):
    # Рандомный комплимент из texts.py
    rand_comp = random.choice(COMPLIMENTS)
    await message.answer(rand_comp)

    # Рандомная фотка из images
    rand_img = random.choice(files_img)
    await bot.send_photo(message.from_user.id,
                         photo=types.InputFile(f'images/{rand_img}'))


# Создает InlineKeyboardMarkup для ответов в викторине
def create_ikb(answers: list, correct_answer: str) -> types.InlineKeyboardMarkup:
    '''
    Функция возвращает экземпляр класса InlineKeyboardMarkup.
    Создает кнопки из списка ответов, присваивая callback_data='correct_answer'
    правильному ответу, а не правильным 'wrong_answer'.
    '''
    keyboard = types.InlineKeyboardMarkup()
    for answer in answers:
        if answer == correct_answer:
            button = types.InlineKeyboardButton(text=answer,
                                                callback_data='correct_answer')
        else:
            button = types.InlineKeyboardButton(text=answer,
                                                callback_data='wrong_answer')
        keyboard.add(button)
    return keyboard


@dp.message_handler(Text('Викторина'))
async def start_quiz(message: types.Message):
    # Кнопка запуска викторины
    start_quiz_kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Я готова! Начинаем.',
                                        callback_data='correct_answer')
    start_quiz_kb.add(button)

    # Определяем id пользователя и создаем словарь количества правильных ответов
    user_id = message.from_user.id
    results[user_id] = 0

    # Создаем KeyboardButton для возвращения в главное меню
    menu_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_kb.add(types.KeyboardButton('Главное меню'))

    await message.answer(f'Количество вопросов: {len(QUIZ)}', reply_markup=menu_kb)
    await message.answer('Для успешного прохождения, тебе нужно ответить на все вопросы без ошибок!!! И получишь подарок 🎁',
                         reply_markup=start_quiz_kb)


@dp.callback_query_handler(text='correct_answer')
async def get_question(callback_query: types.CallbackQuery):
    '''
    Обработчик правильных ответов,
    при каждом правильном ответе счетчик увеличивается на еденицу
    и выводится новый вопрос.
    '''

    # Определяем id пользователя и количество правильных ответов
    user_id = callback_query.from_user.id
    number_correct_answers = results.get(user_id)

    # Контроллер сообщений
    if number_correct_answers == 0:
        banner = 'Стартуем! Удачи'
    else:
        banner = 'Правильный ответ'

    # Проверка на количество полученных вопросов
    if number_correct_answers < len(QUIZ):
        await callback_query.answer(banner)
        results[user_id] += 1

        # Получаем вопрос, ответы и правильный ответ из нашей коллекции вопросов
        question_text = QUIZ[number_correct_answers]["question"]
        answers = QUIZ[number_correct_answers]["answers"]
        correct_answer = QUIZ[number_correct_answers]["correct_answer"]

        # Формируем нужную нам клавиатуру
        keyboard = create_ikb(answers, correct_answer)

        # Изменяем предыдущий вопрос
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=question_text,
                                    reply_markup=keyboard)
    else:
        await callback_query.message.delete()
        await callback_query.message.answer('Ты прошла викторину 👏, парень должен тебе подарок!',
                                            reply_markup=main_menu())


@dp.callback_query_handler(text='wrong_answer')
async def incorrect_ans(callback: types.CallbackQuery):
    '''
    Обработчик неправильных ответов,
    тут все просто, при получение неправильного ответа выходим в галвное меню.
    '''
    await callback.message.answer('Это был неправильный ответ. Боль, печаль, сегодня без подарка 😢',
                                  reply_markup=main_menu())
    await callback.message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    '''
    Обработчик всех остальных сообщений.
    '''
    await message.answer(text='Мадмуазель нажимайе только на кнопочки))')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
