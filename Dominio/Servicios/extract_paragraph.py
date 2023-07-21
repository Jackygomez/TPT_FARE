from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.clear_respond import format_text
from Adapters import adapter_ls
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

parameters = load_parameters()

def extract(parameters: str, task: str) -> str:
    """
    Split the text in a list of sentences.
    this is a special case for the text category 16
    so we need to split the text in parts
    for now, add the new tasks here for instance
    TIME, CHANGE, CANCELLATION, FUELSURCHARGE, DEPARTUREDATE
    Args:content: String with the text.
    Returns: List of sentences.
    """

    # Usar un diccionario para mapear las tareas a las funciones correspondientes
    task_functions = {
        "TIME": lambda parameters: parameters,
        "CHANGE": lambda parameters: task_change(parameters, "CHANGE"),
        "CANCELLATION": lambda parameters: task_change(parameters, "CANCELLATION"),
        "FUELSURCHARGE": lambda parameters: extract_fuel_surcharge(parameters),
        "DEPARTUREDATE": lambda parameters: extract_departure_date(parameters)
    }

    # Usar el método get del diccionario para obtener la función adecuada o devolver None si no existe
    task_function = task_functions.get(task.upper())

    # Si la función existe, llamarla con los parámetros y devolver el resultado
    if task_function:
        response = task_function(parameters)

    # Si no existe, devolver un mensaje de error o una respuesta vacía
    else:
        response = "Tarea no reconocida"

    return response

# Definir las funciones auxiliares para extraer la información relevante de cada tarea


def extract_fuel_surcharge(parameters):
    select_text = text_segementation("text_category_12", "FUEL", parameters)
    if len(select_text) > 0:
        response = {"FUELSURCHARGE": select_text}
    elif len(parameters["text_category_12"]) > 2000:
        response = {"FUELSURCHARGE": parameters["text_category_12"][:2000]}
    else:
        response = {"FUELSURCHARGE": parameters["text_category_12"]}
    return response


def extract_departure_date(parameters):
    select_text = text_segementation(
        "text_category_12", "DEPARTURE", parameters)
    if len(select_text) > 0:
        response = {"DEPARTUREDATE": select_text}
    else:
        response = {"DEPARTUREDATE": parameters["text_category_12"]}
    return response

def task_change(text: str, task: str) -> dict:
    """
    Split the text in a list of sentences.
    Args:content: String with the text.
    """
    logging.warning("Executing Change and Cancel Extraction")
    content = text
    paragraph = task.upper()
    index_change = content.index("CHANGE")
    index_cancellation = content.index("CANCELLATION")

    if index_cancellation < index_change:
        cancellations = content[0:index_change]
        changes = content[index_change:]
    else:
        changes = content[0:index_cancellation]
        cancellations = content[index_cancellation:]

    dict_split_text = {"CANCELLATION": cancellations, "CHANGE": changes}
    respond = dict_split_text[paragraph]

    if len(respond) > 5000:
        # logging.warning("ActivitiesExtractParagraph: Text is too long, summarizing")
        # respond = adapter_ls.main(respond)
        logging.warning("ActivitiesExtractParagraph: Text is too long, truncating")
        respond = respond[:5000]
    return respond


def text_segementation(category: str, word_to_search: str, parameters: dict) -> str:
    """
    Split the text in a list of sentences.
    Args:content: String
    """
    logging.warning("Executing Fuel Surcharge Extraction")
    content = format_text(parameters[category], False)
    positions = [i for i, word in enumerate(content.split()) if word == word_to_search]
    long_text = 20
    list_paragraphs = []
    for position in positions:
        pre = content.split()[position : position - long_text : position]
        words = content.split()[position : position + long_text]
        paragraph = " ".join(pre + words)
        list_paragraphs.append(paragraph)

    full_text = " ".join(list_paragraphs)
    return full_text
