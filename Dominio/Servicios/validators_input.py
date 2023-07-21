import logging
import os
import re
import sys
from authlib.jose import jwt
from jsonschema import validate

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Entidades.dto_input import (
    schema_input,
    schema_information,
    schema_passengerChild,
    schemma_penaltyText,
    schema_categories
)

from Dominio.Servicios.load_parameter import load_parameters
from Adapters.adapter_auth import get_jwk

parameters = load_parameters()


def get_parameter(req: object, parameter: str) -> str:
    """
    get the parameter from the request
    Args:
        req: request, parameter: parameter to get
    Returns:
        parameter string
    """
    parameter_string = req.params.get(parameter)
    if not parameter_string:
        try:
            req_body = req.get_json()
        except ValueError:
            raise ValueError("Request body must be valid JSON")
        else:
            parameter_string = req_body.get(parameter)
    return parameter_string


def validate_req(req) -> bool:
    """
    this function validate the information of the request
    Args:
        req: request
    Returns:
        dict with the parameters
    """
    parameter_task = get_parameter(req, "task")
    correct_task = validate_task(parameter_task)
    logging.info("======================================")
    logging.warning("correct_task: " + str(correct_task))
    parameter_information = get_parameter(req, "information")
    parameter_penalty_text = get_parameter(req, "penaltyText")
    fare_basis = str(parameter_penalty_text[0]["fareBasis"])
    correct_penalty = validate_text(parameter_penalty_text)
    logging.warning("correct_penalty: " + str(correct_penalty))
    correct_information = validate_text(parameter_information)
    logging.warning("correct_information: " + str(correct_information))
    logging.warning("fareBasis: " + str(fare_basis))
    logging.info("information: " + str(parameter_information))
    logging.info("parameter_penalty_text: " + str(parameter_penalty_text))
    logging.info("======================================")
    if correct_task and correct_penalty and correct_information:
        return True
    else:
        return False


def validate_task(parameter_task: str):
    list_tasks = parameters["list_tasks"]
    if parameter_task not in list_tasks:
        return False
    else:
        return True


def validate_text(parameter_text: str):
    if parameter_text is None:
        return False
    elif parameter_text == "":
        return False
    else:
        return True


def validate_token(token: str) -> bool:
    """
    this function validate the token
    Args:
        token: token
    Returns:
        bool
    """
    if token is None:
        return False
    try:
        logging.warning("validate_token")
        jwk = get_jwk()
        token = token.replace("Bearer ", "")
        claims = jwt.decode(token, jwk)
        claims.validate()
        logging.info("token validated")
        return True
    except Exception as e:
        logging.error(e)
        return False


def validate_schema(parameter_information, parameter_penalty_text):
    """
    This function validate the schema of the information and penaltyText
    Args: parameter_information, parameter_penalty_text
    Returns: None
    """
    validate(instance=parameter_information, schema=schema_information)
    pasenger_child = parameter_information["passengerChild"]
    for passenger in pasenger_child:
        validate(
            instance=passenger, schema=schema_passengerChild)
    for parameter in parameter_penalty_text:
        validate(instance=parameter, schema=schemma_penaltyText)

    list_categories = parameter_penalty_text[0]["categories"]
    for categories in list_categories:
        validate(instance=categories, schema=schema_categories)


def validate_strings_in_dict(dict_test: dict):
    """
    This function validate the strings in the dict
    Args: dict_test
    Returns: None
    """
    special_chars = set("{}[]()<>@`=+|!#$%^&*,\\\\")
    response = True
    for key, value in dict_test.items():
        if isinstance(value, str) and any(c in special_chars for c in value):
            logging.error(f"value: {value} contains special characters")
            response = False
    if not response:
        raise ValueError("value contains special characters")
