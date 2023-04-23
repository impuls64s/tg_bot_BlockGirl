from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup


def main_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Флирт с джентельменом 🤭')
    button2 = KeyboardButton('Получить комплимент 😍')
    button3 = KeyboardButton('Покажи фотку')
    button4 = KeyboardButton('Викторина')
    keyboard.add(button1, button2).add(button3, button4)
    return keyboard


def start_quiz_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Я готова! Начинаем.',
                                  callback_data='start_quiz')
    keyboard.add(button)
    return keyboard


def quiz_end_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Закончить викторину')
    keyboard.add(button)
    return keyboard


def answer_kb(answers: list, correct_answer: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for answer in answers:
        if answer == correct_answer:
            answer_options = 'correct_answer'
        else:
            answer_options = 'wrong_answer'
        button = InlineKeyboardButton(text=answer,callback_data=answer_options)
        keyboard.add(button)
    return keyboard

