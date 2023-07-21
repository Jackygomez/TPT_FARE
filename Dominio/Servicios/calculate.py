from statistics import mean
import logging


def overall_average(respuesta: list) -> float:
    """
    This function is for calculate the overall
    average of the respond of the GPT.
    Args:
        respuesta (dict): This is a dictionary
        with the respond of the GPT.
    Returns:
        float: This is a float with the overall
        average of the respond of the GPT.
    """

    logging.info("Executing overall_average")
    list_true_answers = []
    try:


        # Usar comprensión de listas en lugar de un bucle for
        list_true_answers = [value["meanProbability"]
                            for value in respuesta if value["meanProbability"] != 0]

        # Usar la función incorporada mean en lugar de sumar y dividir
        average = mean(list_true_answers)

        return average
    except Exception:
        return 0
