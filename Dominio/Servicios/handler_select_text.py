import logging

from Dominio.Servicios.load_parameter import load_parameters

parameter = load_parameters()


def search_key(dict_penalty: dict, key_input: str) -> list:
    """
    search farebasis in a json
    Args:
        dict_penalty: json
    Returns:
        list of farebasis
    """
    return dict_penalty.get(key_input)


def remove_duplicate_passenger(penalty_text: list, list_passenger_type: list) -> list:
    """
    remove duplicate passenger types
    Args:
        penalty_text: list of jsons
        list_passenger_type: list of passenger types
    Returns:
        list of jsons
    """

    # Convertir la lista de tipos de pasajeros en un conjunto para mejorar la eficiencia
    set_passenger_type = set(list_passenger_type)

    list_clean = []
    for dict_penalty in penalty_text:
        passenger_type = dict_penalty["passengerTypes"]
        # Verificar si el primer tipo de pasajero está en el conjunto y eliminarlo si es así
        if passenger_type[0] in set_passenger_type:
            set_passenger_type.remove(passenger_type[0])
            list_clean.append(dict_penalty)
    return list_clean


# Usar comprensión de diccionarios y conjuntos en lugar de bucles for y listas
def extract_categories(dict_penalty: dict) -> dict:
    """
    This extract the categories from the json
    Args: dict_penalty (dict): This is a dictionary
    with the categories
    Returns: result (dict): This is a dictionary
    with the categories
    """

    # Obtener las categorías del diccionario de penalización
    categorias = dict_penalty["categories"]

    # Crear un diccionario con el código y el texto libre de cada categoría
    text_category = {
        dict_category["code"]: dict_category["freeText"] for dict_category in categorias}

    # Crear un diccionario con el nombre y el código de cada categoría
    name_category = {
        "name_" + dict_category["code"]: dict_category["name"] for dict_category in categorias}

    # Obtener las categorías validadas del parámetro
    validated_categories = parameter["validated_categories"]

    # Crear un conjunto con los códigos de las categorías validadas
    set_categories = {int(dict_category["code"]) for dict_category in categorias if int(
        dict_category["code"]) in validated_categories}

    # Unir los diccionarios y el conjunto en un solo resultado
    result = {
        **text_category,
        **name_category,
        "list_categories": set_categories,
    }

    return result


def extract_passenger(penalty_text: dict, type_passenger: list) -> list:
    """
    extract dict_penalty by passenger type
    Args:
        dict_penalty: json
    Returns:
        list of adult passenger
    """
    list_clean = []
    for dict_penalty in penalty_text:
        passenger_type = dict_penalty["passengerTypes"]
        passenger_type.sort()
        if passenger_type[0].lower() in type_passenger:
            list_clean.append(dict_penalty)
    return list_clean
