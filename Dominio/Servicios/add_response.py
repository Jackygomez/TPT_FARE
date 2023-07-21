from Dominio.Servicios import build_response
from Dominio.Servicios.validators_respond import validate_date

def build_date_response(departure_date: str, number_question: int) -> dict:
    """
    This function build the response departure date
    Args: departure_date (str): This is a string with the departure date
    Returns: respond (dict):
    """
    date_formated = validate_date(departure_date)

    respond = build_response.edit_response(
        question_input="Departure date?",
        answer_input=date_formated,
        quote_input=departure_date,
        number_question_input=number_question,
        boolean_input=True,
    )
    return respond


def build_refundable_response(
        model_respond: list, number_question: int) -> dict:
    """
    This function build the response refundable
    Args: model_respond (list): This is a list with the respond of the GPT
    Returns: respond (dict):
    This is a dictionary with the respond about the refundable
    """

    list_questions = []
    
    text_to_validate = ""
    boolean_2 = False
    for response in model_respond:
        if "which time you can cancel" in response["question"].lower():
            list_questions.append(response)
            text_to_validate = response["quote"].upper(
            ) + " " + response["answer"][0].upper()
        if "charge for cancel" in response["question"].lower():
            list_questions.append(response)
            boolean_2 = response["boolean"]

    is_anytime = False
    if 'ANY' in text_to_validate:
        is_anytime = True
    if 'BEFORE' in text_to_validate:
        is_anytime = True

    validate = boolean_2 and is_anytime

    respond = build_response.edit_response(
        question_input="Is refundable?",
        answer_input="Refundable" if validate else "Not Refundable",
        category_input=16,
        number_question_input=number_question,
        boolean_input=validate,
        quote_input=response["quote"])

    return respond
