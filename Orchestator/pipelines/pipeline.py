import azure.durable_functions as df
import os
import sys
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_response import (
    set_category,
    set_free_text,
    set_model_respond,
)
from Dominio.Servicios.sort_dates import set_days, set_date
from Dominio.Servicios.sort_text_to_model import data_question_category, join_text
from Dominio.Servicios.add_response import (
    build_date_response,
    build_refundable_response,
)

parameters = load_parameters()


def pipeline(context: df.DurableOrchestrationContext, parameters_dict: dict):
    """
    This is the main pipeline function. Execute in parallel the activities
    Args:
        context (DurableOrchestrationContext):
        The context object for durable function
        parameters_dict (dict): This is a dictionary with the parameters
    Returns:
        parameters_dict: This is a dictionary with the respond of the GPT
    #"""

    list_weeks = parameters["weeks"]
    list_to_format_dates = parameters["category_to_format_date"]
    list_to_days = parameters["category_to_days"]
    task = parameters_dict["task"]
    category_data = data_question_category(parameters, parameters_dict)
    question_category_dict = category_data["question_category_dict"]
    general_question_category_dict = category_data[
            "general_question_category_dict"]
    dict_to_quiz = {
        "question_category_dict": question_category_dict,
        "parameters_dict": parameters_dict,
    }
    parameters_quiz = yield context.call_activity(
        "ActivitiesSortParametersQuiz", dict_to_quiz
    )

    list_quiz_response = []
    list_quiz_response = [context.call_activity(
        "ActivitiesExecuteQuiz", parameter) for parameter in parameters_quiz]
    outputs = yield context.task_all(list_quiz_response)
    list_gpt_responses = join_and_sort_dict(outputs)
    list_categories = general_question_category_dict[
            "number_questions_with_category"]
    list_categories = set_questions_category_19(
            list_categories, list_gpt_responses)
    list_free_text = set_free_text(parameters_dict, list_categories)
    set_category(list_gpt_responses, list_categories)
    set_date(list_gpt_responses, list_to_format_dates)
    set_days(list_gpt_responses, list_to_days, list_weeks)
    model_respond = set_model_respond(list_gpt_responses)
    build_responses(model_respond, parameters_dict, task)
    data_respond = {
        "parameters_dict": parameters_dict,
        "list_free_text": list_free_text,
        "model_respond": model_respond,
    }
    respuesta = yield context.call_activity(
            "ActivitiesSortAnswer",
            data_respond)
    return respuesta


def sort_parameters_quiz(
        parameters_dict: dict, question_category_dict: dict) -> dict:
    """
    This function sorts the parameters to execute the quiz
    Args: parameters_dict: dictionary with the parameters
    Return: parameters_quiz: dictionary with the parameters to execute the quiz
    """

    quiz_text_and_question = join_text(question_category_dict)["text"]

    list_categories = question_category_dict["number_questions_with_category"]

    number_questions = question_category_dict["len_questions_lite"]

    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": number_questions,
        "list_questions": question_category_dict["questions_lite"],
        "task": parameters_dict["task"],
        "list_categories": list_categories,
    }
    return parameters_quiz


def join_and_sort_dict(list_dict: list) -> dict:
    """
    This function joins the dictionaries in the list
    Args: list_dict: list of dictionaries
    Return: dict_join: dictionary with the dictionaries in the list
    """
    dict_join = {}
    count = 1

    for dict_question in list_dict:
        for key, value in dict_question.items():

            new_key = "question" + "_" + str(count)
            dict_join[new_key] = value
            value["numberQuestion"] = count
            count += 1

    return dict_join


def build_responses(model_respond: list, parameters_dict: dict, task: str):
    """
    This function builds the responses of the model
    Args:
        model_respond (list): list with the responses of the model
        parameters_dict (dict): dictionary with the parameters
        task (str): task of the conversation
    """
    if task.upper() == "CHANGE":
        departure_date = parameters_dict["data_information"]["departureDate"]
        departure_date_response = build_date_response(
            departure_date, len(model_respond) + 1
        )
        model_respond.append(departure_date_response)
    if task.upper() == "CANCELLATION":
        question_refundable = build_refundable_response(
            model_respond, len(model_respond) + 1
        )
        model_respond.append(question_refundable)


def set_questions_category_19(
        list_categories: list,
        list_gpt_responses: list):
    """
    This function sets the category 19 to the questions
    Args: list_categories: list with the categories
    Return: list_categories: list with the categories
    """

    if len(list_categories) < len(list_gpt_responses) and 19 not in list_categories:
        list_categories = list_categories * len(list_gpt_responses)

    if 19 in list_categories:

        list_sorted_categories = []

        for key, value in list_gpt_responses.items():

            if "CHILDREN DISCOUNTS" in value["question"]:
                list_sorted_categories.append(19)
            else:
                list_sorted_categories.append(16)

        list_categories = list_sorted_categories

    if 16 in list_categories and 19 not in list_categories:
        list_categories = [16] * len(list_gpt_responses)

    return list_categories
