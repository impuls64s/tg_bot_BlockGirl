import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from keyboards import answer_kb, END_QUIZ_KB, MAIN_KB, START_QUIZ_KB
from texts import bot_answers as ba, flirting, stikers, quiz
from utils import current_question, get_random_photo


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)

results = dict()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(text=ba.HELP_CMD,
                        reply_markup=MAIN_KB,
                        parse_mode="HTML")


@dp.message_handler(Text('Покажи фотку'))
async def send_photo(message: types.Message):
    await message.answer_photo(photo=types.InputFile(get_random_photo()))


@dp.message_handler(Text('Флирт с джентельменом 🤭'))
async def send_flirt(message: types.Message):
    random_flirt = random.choice(flirting.FLIRT)
    await message.answer(random_flirt)

    random_sticker = random.choice(stikers.BUMS)
    await message.answer_sticker(sticker=random_sticker)


@dp.message_handler(Text('Получить комплимент 😍'))
async def send_compliment(message: types.Message):
    random_compliment = random.choice(flirting.COMPLIMENTS)
    await message.answer_photo(photo=types.InputFile(get_random_photo()),
                               caption=random_compliment)


@dp.message_handler(Text('Викторина'))
async def start_quiz(message: types.Message):
    await message.answer(f'Количество вопросов: {len(quiz.IT)}',
                         reply_markup=END_QUIZ_KB)
    await message.answer(text=ba.QUIZ_DESCRIPTION,
                         reply_markup=START_QUIZ_KB)


@dp.message_handler(Text('Закончить викторину'))
async def end_quiz(message: types.Message):
    await message.reply(text='Викторина окончена.', reply_markup=MAIN_KB)


@dp.callback_query_handler(text='start_quiz')
async def first_question(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    results[user_id] = 0

    question_text, list_answers, correct_answer = current_question(0)
    keyboard = answer_kb(list_answers, correct_answer)
    await callback_query.message.edit_text(text=question_text,
                                           reply_markup=keyboard)


@dp.callback_query_handler(text='correct_answer')
async def next_question(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    results[user_id] += 1
    number_correct_answers = results.get(user_id)
    nnq = number_correct_answers  # next number question

    if number_correct_answers < len(quiz.IT):
        await callback_query.answer(text='Правильный ответ')

        question_text, list_answers, correct_answer = current_question(nnq)
        keyboard = answer_kb(list_answers, correct_answer)
        await callback_query.message.edit_text(text=question_text,
                                               reply_markup=keyboard)
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(text=ba.WIN_QUIZ,
                                            reply_markup=MAIN_KB)


@dp.callback_query_handler(text='wrong_answer')
async def losing_quiz(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text=ba.LOSING_QUIZ,
                                        reply_markup=MAIN_KB)
    await callback_query.message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=ba.ONLY_BUTTONS)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
