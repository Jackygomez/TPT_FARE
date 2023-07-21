import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


from Dominio.Servicios.handler_respond import individual_paragraphs
from Adapters import adapter_azure_gpt as adapter


from Dominio.Servicios.load_parameter import load_parameters

loaded_parameters = load_parameters()


def main(parameters: dict) -> dict:
    """
    This is a function for send a GPT a text and get a respond.
    Args:
        parameterscancellation (dict): This is a dictionary with text and task.
    Returns:
        dict: This is a dictionary with text and mean probability.
    """

    logging.warning("Executing ActivitiesExtractParagraph")
    quiz_text_and_question = parameters["quiz_text_and_question"]
    logging.warning("quiz_text_and_question")
    logging.warning("====================================")
    logging.info(quiz_text_and_question)
    logging.warning("====================================")
    task = parameters["task"]
    gpt_quiz = adapter.ask_openai(quiz_text_and_question, task)
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]
    number_questions = parameters["number_questions"]
    list_questions = parameters["list_questions"]

    respond = individual_paragraphs(
        gpt_quiz_text, gpt_quiz_mean_probability, parameters, task, number_questions, list_questions
    )
    return respond
