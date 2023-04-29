import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import answer_kb, END_QUIZ_KB, MAIN_KB, START_QUIZ_KB
from texts import bot_answers as ba, flirting, stikers, quiz
from utils import current_question, get_random_photo, QuizState

QUIZ_LENGTH = len(quiz.IT)


async def cmd_start(message: types.Message):
    await message.reply(text=ba.HELP_CMD,
                        reply_markup=MAIN_KB,
                        parse_mode="HTML")


async def end_quiz(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(text='Викторина окончена.', reply_markup=MAIN_KB)


async def send_photo(message: types.Message):
    await message.answer_photo(photo=types.InputFile(get_random_photo()))


async def send_flirt(message: types.Message):
    random_flirt = random.choice(flirting.FLIRT)
    await message.answer(random_flirt)

    random_sticker = random.choice(stikers.BUMS)
    await message.answer_sticker(sticker=random_sticker)


async def send_compliment(message: types.Message):
    random_compliment = random.choice(flirting.COMPLIMENTS)
    await message.answer_photo(photo=types.InputFile(get_random_photo()),
                               caption=random_compliment)


async def start_quiz(message: types.Message):
    await QuizState.start_quiz.set()
    await message.answer(f'Количество вопросов: {len(quiz.IT)}',
                         reply_markup=END_QUIZ_KB)
    await message.answer(text=ba.QUIZ_DESCRIPTION,
                         reply_markup=START_QUIZ_KB)


async def first_question(callback_query: types.CallbackQuery,
                         state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        data[user_id] = 0

    await QuizState.next()
    question_text, list_answers, correct_answer = current_question(0)
    keyboard = answer_kb(list_answers, correct_answer)
    await callback_query.message.edit_text(text=question_text,
                                           reply_markup=keyboard)


async def next_question(callback_query: types.CallbackQuery,
                        state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        data[user_id] += 1

    number_correct_answers = data.get(user_id)
    nnq = number_correct_answers  # next number question

    if number_correct_answers < QUIZ_LENGTH:
        await callback_query.answer(text='Правильный ответ')

        question_text, list_answers, correct_answer = current_question(nnq)
        keyboard = answer_kb(list_answers, correct_answer)
        await callback_query.message.edit_text(text=question_text,
                                               reply_markup=keyboard)
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(text=ba.WIN_QUIZ,
                                            reply_markup=MAIN_KB)
        await state.finish()
        await callback_query.message.answer_video(
            video=types.InputFile('videos/win_quiz.mp4')
            )


async def losing_quiz(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer(text=ba.LOSING_QUIZ,
                                        reply_markup=MAIN_KB)
    await callback_query.message.delete()


async def echo(message: types.Message):
    await message.answer(text=ba.ONLY_BUTTONS)
