from Dominio.Servicios import handler_select_text

def iterate_penalty_text(
    penalty_text: list, parameter_information: str, is_child: bool
) -> list:
    """
    iterate over the penalty text and execute the pipeline
    Args:
        penalty_text: list of jsons
    Returns:
        list of gpt responses
    """

    for dict_penalty in penalty_text:
        dict_response = iterate_categories_in_penalties(
            dict_penalty, parameter_information, is_child
        )

    return dict_response


def iterate_categories_in_penalties(
    dict_penalty: dict, parameter_information: str, is_child: bool
) -> dict:
    """
    iterate over the categories and execute the pipeline
    Args:
        dict_penalty: a dictionary with penalty information
        parameter_information: a string with additional information
        is_child: a boolean indicating if the penalty is a child of another one
    Returns:
        a dictionary with parameters for the pipeline
    """

    # extract categories from dict_penalty
    result_categories = handler_select_text.extract_categories(dict_penalty)

    # create a dictionary with parameters for the pipeline
    dict_parameters = {
        "data_information": parameter_information,
        "is_child": is_child,
        "dict_penalty": dict_penalty,
        "list_categories": result_categories["list_categories"]
    }

    # add text and name of each category to the dictionary
    for key, value in result_categories.items():
        if key.isnumeric():
            dict_parameters[f"text_category_{key}"] = value
            dict_parameters[f"name_category_{key}"] = result_categories[f"name_{key}"]

    return dict_parameters
