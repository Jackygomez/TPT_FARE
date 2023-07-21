import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_text_to_model import join_text

parameters = load_parameters()


def main(parameters: dict) -> list:
    logging.warning("Start Activity Sort Parameters Quiz")
    question_category_dict = parameters["question_category_dict"]
    parameters_dict = parameters["parameters_dict"]
    list_parameters_quiz = []
    for key, value in question_category_dict.items():
        parameters_quiz = sort_parameters_quiz(parameters_dict, value)
        list_parameters_quiz.append(parameters_quiz)
    return list_parameters_quiz


def sort_parameters_quiz(parameters_dict: dict, question_category_dict: dict):
    quiz_text_and_question = join_text(question_category_dict)["text"]
    list_categories = question_category_dict["number_questions_with_category"]

    number_questions = question_category_dict["len_questions_lite"]

    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": number_questions,
        "list_questions": question_category_dict["questions_lite"],
        "task": parameters_dict["task"],
        "list_categories": list_categories
    }
    return parameters_quiz
