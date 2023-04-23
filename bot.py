import os
import random
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from utils import random_photo, current_question
from texts import bot_answers, flirting, stikers, quiz
from keyboards import main_kb, start_quiz_kb, quiz_end_kb, answer_kb

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)

# Keyboards
MAIN_KB = main_kb()
START_QUIZ_KB = start_quiz_kb()
END_QUIZ_KB = quiz_end_kb()

results = dict()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(text=bot_answers.HELP_CMD,
                        reply_markup=MAIN_KB,
                        parse_mode="HTML")


@dp.message_handler(Text('Покажи фотку'))
async def send_photo(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=types.InputFile(random_photo()))


@dp.message_handler(Text('Флирт с джентельменом 🤭'))
async def send_flirt(message: types.Message):
    random_flirt = random.choice(flirting.FLIRT)
    await message.answer(random_flirt)

    random_sticker = random.choice(stikers.BUMS)
    await bot.send_sticker(message.from_user.id, sticker=random_sticker)


@dp.message_handler(Text('Получить комплимент 😍'))
async def send_compliment(message: types.Message):
    random_compliment = random.choice(flirting.COMPLIMENTS)
    await message.answer(random_compliment)

    await bot.send_photo(message.from_user.id,
                         photo=types.InputFile(random_photo()))


@dp.message_handler(Text('Викторина'))
async def start_quiz(message: types.Message):
    await message.answer(f'Количество вопросов: {len(quiz.IT)}',
                         reply_markup=END_QUIZ_KB)
    await message.answer('Для успешного прохождения, тебе нужно ответить на все вопросы без ошибок!!! И получишь подарок 🎁',
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

    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=question_text,
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

        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=question_text,
                                    reply_markup=keyboard)
    else:
        await callback_query.message.delete()
        await callback_query.message.answer('Ты прошла викторину 👏, парень должен тебе подарок!',
                                            reply_markup=MAIN_KB)


@dp.callback_query_handler(text='wrong_answer')
async def losing_quiz(callback: types.CallbackQuery):
    await callback.message.answer('Это был неправильный ответ. Боль, печаль, сегодня без подарка 😢',
                                  reply_markup=MAIN_KB)
    await callback.message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text='Мадмуазель нажимайе только на кнопочки))')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
