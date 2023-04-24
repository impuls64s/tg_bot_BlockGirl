import os
import random

from dotenv import load_dotenv

from texts import quiz

load_dotenv()


def get_random_photo() -> str:
    photo_dirs = os.getenv('PHOTOS_DIRECTORY')
    if not os.path.exists(photo_dirs):
        raise Exception('No photo directory')

    list_photo = os.listdir(photo_dirs)
    if not list_photo:
        raise Exception('Photo folder is empty')

    random_photo = random.choice(list_photo)
    path_photo = os.path.join(photo_dirs, random_photo)
    return path_photo


def current_question(question_number: int) -> tuple[str, list, str]:
    quiz_number = quiz.IT[question_number]
    question_text = quiz_number.get("question")
    list_answers = quiz_number.get("answers")
    correct_answer = quiz_number.get("correct_answer")
    return question_text, list_answers, correct_answer
