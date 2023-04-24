from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)


MAIN_KB = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('Флирт с джентельменом 🤭')
button2 = KeyboardButton('Получить комплимент 😍')
button3 = KeyboardButton('Покажи фотку')
button4 = KeyboardButton('Викторина')
MAIN_KB.add(button1, button2).add(button3, button4)


START_QUIZ_KB = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Я готова! Начинаем.',
                              callback_data='start_quiz')
START_QUIZ_KB.add(button)


END_QUIZ_KB = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton('Закончить викторину')
END_QUIZ_KB.add(button)


def answer_kb(answers: list, correct_answer: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for answer in answers:
        if answer == correct_answer:
            answer_options = 'correct_answer'
        else:
            answer_options = 'wrong_answer'
        button = InlineKeyboardButton(text=answer,
                                      callback_data=answer_options)
        keyboard.add(button)
    return keyboard
