import os
import sys
import azure.durable_functions as df

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios import handler_select_text
from Dominio.Servicios import object_iterator
from pipelines import pipeline

parameters = load_parameters()


def orchestrator_function(
    context: df.DurableOrchestrationContext,
) -> dict:

    parameters = context.get_input()
    parameter_task = parameters["task"]
    parameter_information = parameters["information"]
    parameter_penalty_text = parameters["penaltyText"]

    list_passengers_type = []
    list_passengers = []
    list_farebasis = []
    list_passengers = [passenger for dict_penalty in parameter_penalty_text for passenger in handler_select_text.search_key(
        dict_penalty, 'passengerTypes')]


    list_farebasis = [handler_select_text.search_key(
        dict_penalty, 'fareBasis') for dict_penalty in parameter_penalty_text]
    list_passengers_type = list(set(list_passengers))
    is_child = validate_child(list_passengers_type)
    passengers_type = tuple(list_passengers_type)


    parameter_penalty_text = handler_select_text.remove_duplicate_passenger(
        parameter_penalty_text, list_passengers_type
    )

    parameter_penalty_text = handler_select_text.extract_passenger(
        parameter_penalty_text, ["adult", "child"]
    )

    parameters_object = object_iterator.iterate_penalty_text(
        parameter_penalty_text, parameter_information, is_child
    )

    parameters_object["task"] = parameter_task
    parameters_object["dict_penalty"]["passengerTypes"] = list(passengers_type)
    parameters_object["dict_penalty"]["fareBasis"] = list_farebasis
    parameters_object["dict_penalty"]["listPassengers"] = list_passengers

    gpt_response = pipeline.pipeline(context, parameters_object)
    return gpt_response


main = df.Orchestrator.create(orchestrator_function)


def validate_child(list_passenger: list) -> bool:
    """
    Validate if the passenger is a child or infant
    Args:list_passenger: list of passenger types
    Returns: True if the passenger is a child or infant
    """
    return any("child" in passenger_type.lower() or "infant" in passenger_type.lower() for passenger_type in list_passenger)
