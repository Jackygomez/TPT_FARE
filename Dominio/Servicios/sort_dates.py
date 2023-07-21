import datetime
import re


def build_dates(str_date: str) -> list:
    """
    This function receives a string with dates 
    and returns a list with the dates
    Args: str_date (str): String with dates
    return: list_dates (list): List with dates
    """
    list_dates = search_date(str_date)
    list_format_dates = []
    for date in list_dates:
        list_format_dates.append(str_to_datetime(date))
    return list_format_dates


def str_to_datetime(date_str: str) -> datetime:
    """
    This function receives a string with date
    and returns a datetime object
    Args: date_str (str): String with date
    return: date (datetime): Datetime object
    """
    date_str = date_str.upper()
    day = re.findall(r"\d{2}", date_str)[0]
    month = re.sub(r"\d{2}", "", date_str)
    year = datetime.datetime.now().year
    date = datetime.datetime.strptime(f"{day}/{month}/{year}", "%d/%b/%Y")
    date = date.strftime("%d/%m/%Y")
    return date


def search_date(date_str: str) -> list:
    """
    This function receives a string with dates
    for example 10SEP and returns a list with the dates
    Args: date_str (str): String with dates
    return: list_dates (list): List with dates
    """
    date_str = date_str.upper()
    date_str = re.sub(r"[^\w\s]", "", date_str)
    list_dates = re.findall(r"\d{2}[A-Z]{3}", date_str)
    return list_dates


def set_date(dict_question: dict, list_question_date: list):
    """
    This functios is used to extract the dates in the questions
    Args: list_question: list of questions
    list_question_date: list of questions with dates
    """
    for key, value in dict_question.items():
        if value["category"] in list_question_date:
            if len(value["quote"]) > len(value["answer"][0]):
                list_format_dates = build_dates(value["quote"])
            else:
                list_format_dates = build_dates(value["answer"][0])
            if len(list_format_dates) > 0:
                value["value"] = list_format_dates


def set_days(dict_question: dict, list_question_week: list, list_weeks: list):
    """
    This function is used to extract the weeks in the questions
    Args: list_question: list of questions
    list_question_week: list of questions with weeks
    """
    response = []
    for key, value in dict_question.items():
        if value["category"] in list_question_week:
            #quitar signos de puntuación
            text_value = re.sub(r"[^\w\s]", "", value["answer"][0])
            text_split = text_value.split(" ")
            for text in text_split:
                print(text)
                if text.upper() in list_weeks:
                    response.append(text)
            value["value"] = response
