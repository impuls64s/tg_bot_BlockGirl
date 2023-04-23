import os
import random
import pathlib
from typing import List

from dotenv import load_dotenv

from texts import quiz

load_dotenv()


def random_photo() -> str:
    photo_dirs = os.getenv('PHOTOS_DIRECTORY')
    if os.path.exists(photo_dirs):
        list_photo = os.listdir(photo_dirs)
        if list_photo:
            random_photo = random.choice(list_photo)
            path_photo = pathlib.Path(photo_dirs, random_photo)
            return path_photo


def current_question(question_number: int) -> tuple[str, List, str]:
    first_quiz = quiz.IT[question_number]
    question_text = first_quiz.get("question")
    list_answers = first_quiz.get("answers")
    correct_answer = first_quiz.get("correct_answer")
    return question_text, list_answers, correct_answer
