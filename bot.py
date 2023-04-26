import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from dotenv import load_dotenv

from handlers import (
    cmd_start,
    end_quiz,
    send_photo,
    send_flirt,
    send_compliment,
    start_quiz,
    first_question,
    next_question,
    losing_quiz, echo,
    )
from utils import QuizState


logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


dp.register_message_handler(cmd_start, commands=['start'])

dp.register_message_handler(end_quiz, commands=['cancel'], state='*')
dp.register_message_handler(end_quiz, Text('Закончить викторину'), state='*')

dp.register_message_handler(send_photo, Text('Покажи фотку'))

dp.register_message_handler(send_flirt, Text('Флирт с джентельменом 🤭'))

dp.register_message_handler(send_compliment, Text('Получить комплимент 😍'))

dp.register_message_handler(start_quiz, Text('Викторина'))
dp.register_callback_query_handler(first_question,
                                   Text('start_quiz'),
                                   state=QuizState.start_quiz)
dp.register_callback_query_handler(next_question,
                                   Text('correct_answer'),
                                   state=QuizState.number_correct_answers)
dp.register_callback_query_handler(losing_quiz,
                                   Text('wrong_answer'),
                                   state=QuizState.number_correct_answers)

dp.register_message_handler(echo, state='*')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
