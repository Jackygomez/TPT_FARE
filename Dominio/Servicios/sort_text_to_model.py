import os
import sys
import logging 

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.validators_respond import (
        validate_category_and_questions)
from Dominio.Servicios.extract_paragraph import extract
from Dominio.Servicios.sort_response import replace_information_children


def data_question_category(question_dict: dict, category_dict: dict) -> dict:
    """
    This sort the information about the question and categories
    Args: question_dict (dict): This is a dictionary with the questions
          category_dict (dict): This is a dictionary with the categories
    Returns:
        question_category_dict: This is a dictionary with the questions and
        categories
    """

    number_questions = category_dict["list_categories"]
    task = category_dict["task"].lower()
    number_questions_with_category = validate_category_and_questions(
        task, number_questions, question_dict)
    category_dict["list_categories"] = number_questions_with_category
    passenger_child = category_dict["data_information"]["passengerChild"]
    list_texts_test = []
    list_texts_test = [category_dict["name_category_" + str(
        number)] + "\n" + category_dict["text_category_" + str(number)] for number in number_questions_with_category]
    len_list_text = [len(text) for text in list_texts_test]
    group_categories_index = group_text(len_list_text, 1000)[
        "dict_groups_index"]

    general_data = data_by_group(number_questions_with_category,
                                 category_dict,
                                 question_dict,
                                 task,
                                 passenger_child)
    questions_dict = {}
    for key, value in group_categories_index.items():
        categories = [number_questions_with_category[i] for i in value]
        result = data_by_group(categories,
                               category_dict,
                               question_dict,
                               task,
                               passenger_child)
        questions_dict[key] = result
    return {
        "general_question_category_dict": general_data,
        "question_category_dict": questions_dict
    }


def join_text(dict_list: dict) -> dict:
    """
    This function build the text to send to GPT
    Args: dict_list (dict): This is a dictionary with the list of questions
    Return: questions_dict (dict): This is a dictionary with the text to send
    """

    list_texts = dict_list["list_texts"]
    list_questions = dict_list["list_questions"]
    structure_paragraph_question = dict_list["structure_paragraph_question"]
    structure_fare_rules = dict_list["structure_fare_rules"]
    questions_lite_list = dict_list["questions_lite"]

    text = "\n".join(list_texts)
    questions_text = "\n".join(list_questions)
    questions_dict = {}
    questions_dict["text"] = text + "\n" + structure_paragraph_question + \
        questions_text + "\n" * 2 + structure_fare_rules + "\n" * 2 + \
        "SOLUTION QUESTIONS 1 to {0}".format(len(questions_lite_list))
    return questions_dict


def group_text(test_list: list, long_text: int) -> dict:
    """
    This function groups the text in a list into groups of n characters
    Args: test_list (list): This is a list with the text
    Returns: dict_groups_index (dict): This is a dictionary with the index of
    """
    dict_groups_index = {}
    dict_group_len = {}

    dict_groups_index = {"1": [test_list.index(i) for i in test_list if i <= long_text],
                         "2": [test_list.index(i) for i in test_list if i > long_text]}


    dict_group_len = {"1": [i for i in test_list if i <= long_text],
                    "2": [i for i in test_list if i > long_text]}

    #TODO
    if "1" in dict_groups_index and "2" in dict_groups_index:
        n = 2
    if "1" not in dict_groups_index and "2" in dict_groups_index:
        n = 1
    if "1" in dict_groups_index and "2" not in dict_groups_index:
        n = 2

    if "2" in dict_groups_index:
        list_long_value = dict_groups_index["2"]

        dict_list_long = {}
        longitud = len(list_long_value)
        for i in range(longitud):
            dict_list_long.setdefault(
                str(i + n), []).append(list_long_value[i])

        dict_groups_index.pop("2")
        dict_groups_index.update(dict_list_long)

    return {
        "dict_groups_index": dict_groups_index,
        "len_dict_groups_index": len(dict_groups_index),
        "dict_group_len": dict_group_len,
    }


def data_by_group(
        number_questions_with_category: list,
        category_dict: dict,
        question_dict: dict,
        task: str,
        passenger_child: dict) -> dict:
    """
    This function build the data to send to GPT
    Args:
        number_questions_with_category (list): This is a list
        with the number of categories with questions
        category_dict (dict): This is a dictionary with the categories
        question_dict (dict): This is a dictionary with the questions
        task (str): This is a string with the task
        passenger_child (dict): This is a dictionary with the passenger child
    Returns: question_category_dict (dict):
    This is a dictionary with the questions and categories
    """

    structure_paragraph_question = question_dict["question_paragraph_general"]
    structure_fare_rules = question_dict["structure_fare_rules"]
    question_category_dict = {}
    list_questions = []
    list_texts = []
    questions_lite_list = []

    for number in number_questions_with_category:
        text = "text_category_" + str(number)
        title = "name_category_" + str(number)
        if text in category_dict and category_dict[text] != "":
            questions = question_dict["question_category_" + str(number)][task]
            questions_lite = question_dict["qlite_category_" +
                                           str(number)][task]
            questions_lite_list_split = questions_lite.split("\n")
            text_category = category_dict[text]
            if number == 16:
                text_category = extract(text_category, task)
            # TODO: loogica para crear preguntas de la categoria 19
            if number == 19:
                child_list_questions = []
                child_list_questions = replace_information_children(
                    questions, passenger_child)
                list_questions.extend(child_list_questions)
                questions = ""

                questions_lite_list.extend(child_list_questions)
            questions_lite_list.extend(questions_lite_list_split)
            title_category = category_dict[title]
            question_and_category = title_category + "\n" + \
                text_category + "\n" + questions + 2*"\n"

            question_category_dict["question_category_" +
                                   str(number)] = question_and_category
            question_category_dict["length_category_" +
                                   str(number)] = len(question_and_category)
            list_texts.append(title_category + "\n" + text_category)
            list_questions.append(questions)
    list_questions = list(filter(None, list_questions))
    questions_lite_list = list(filter(None, questions_lite_list))
    questions_lite_list = [
        x for x in questions_lite_list if "#" not in x]

    questions_dict = {}
    questions_dict["questions_lite"] = questions_lite_list
    questions_dict["len_questions_lite"] = len(questions_lite_list)
    questions_dict["list_questions"] = list_questions
    questions_dict["len_list_questions"] = len(list_questions)
    questions_dict[
        "structure_paragraph_question"] = structure_paragraph_question
    questions_dict["structure_fare_rules"] = structure_fare_rules
    questions_dict[
        "number_questions_with_category"] = number_questions_with_category
    questions_dict["list_texts"] = list_texts
    questions_dict["len_passenger_child"] = len(passenger_child)
    return questions_dict
