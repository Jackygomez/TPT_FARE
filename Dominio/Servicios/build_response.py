from Dominio.Entidades import dto_respond


def edit_response(
    question_input=None,
    answer_input=None,
    category_input=None,
    quote_input=None,
    free_text_input=None,
    number_question_input=None,
    boolean_input=None,
    mean_probability_input=None,
    value_input=None,
    denomination_input=None,
) -> dict:
    """
    This function edit the response
    Args:
        inputs
    Returns:
        dict: This is a dictionary with sort of the response
    """

    respond = dto_respond.Respond(
        question="",
        answer=[],
        category=0,
        quote="",
        free_text=False,
        number_question=0,
        boolean=False,
        mean_probability=0,
        value=[],
        denomination=[],
    ).__dict__

    if question_input is not None:
        respond["question"] = question_input
    if answer_input is not None and answer_input != "":
        respond["answer"] = [answer_input] if type(
            answer_input) is not list else answer_input
    if category_input is not None:
        respond["category"] = category_input
    if quote_input is not None:
        respond["quote"] = quote_input
    if free_text_input is not None:
        respond["freeText"] = free_text_input
    if number_question_input is not None:
        respond["numberQuestion"] = number_question_input
    if boolean_input is not None:
        respond["boolean"] = boolean_input
    if mean_probability_input is not None:
        respond["meanProbability"] = mean_probability_input
    if value_input is not None and value_input != "":
        respond["value"] = [value_input] if type(
            value_input) is not list else value_input
    if denomination_input is not None and denomination_input != "":
        respond["denomination"] = (
            [denomination_input] if type(
                denomination_input) is not list else denomination_input
        )

    return respond
