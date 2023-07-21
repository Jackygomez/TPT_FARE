import json
import azure.functions as func
import azure.durable_functions as df
import os
import sys
import logging


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Entidades.error_respond import validate_error
from Dominio.Servicios.validators_input import (
    validate_req,
    validate_schema,
    get_parameter,
    validate_token,
    validate_strings_in_dict)
parameters = load_parameters()


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    try:

        logging.info("Python HTTP trigger function processed a request.")

        correct_req = validate_req(req)
        jwt = req.headers.get("Authorization")
        # is_token = validate_token(jwt)
        is_token = True
        if is_token is False:
            return func.HttpResponse(
                status_code=401, mimetype="application/json"
            )

        if correct_req:
            parameter_task = get_parameter(req, "task")
            parameter_information = get_parameter(req, "information")
            parameter_penalty_text = get_parameter(req, "penaltyText")

            validate_schema(parameter_information, parameter_penalty_text)
            validate_strings_in_dict(parameter_information)
            map(lambda penalty: validate_strings_in_dict(penalty) and map(
                    lambda categories: validate_strings_in_dict(categories),
                    penalty["categories"]), parameter_penalty_text)

            dict_parameters = {
                "task": parameter_task,
                "information": parameter_information,
                "penaltyText": parameter_penalty_text,
            }
            fare_basis = str(parameter_penalty_text[0]["fareBasis"])
            logging.warning("Starter")
            logging.warning(fare_basis)
            client = df.DurableOrchestrationClient(starter)

            instance_id = await client.start_new(
                "Orchestator", None, dict_parameters
            )

            logging.info(f"Started orchestration with ID = '{instance_id}'.")

            respond = await client.get_status(instance_id)

            while respond.runtime_status.value != "Completed":
                respond = await client.get_status(instance_id)
                if respond.runtime_status.value == "Failed":
                    cause = validate_error(respond)

                    return func.HttpResponse(
                        json.dumps({"cause": cause, "error": respond.output}),
                        mimetype="application/json",
                        status_code=500,
                    )
            logging.warning(
                f"Orchestration status: {respond.runtime_status.value}"
            )
            logging.warning("fareBasis: " + str(fare_basis))
            return func.HttpResponse(
                json.dumps(respond.output),
                mimetype="application/json",
                status_code=200,
            )
        else:
            return func.HttpResponse(
                json.dumps(
                    {
                        "cause": (
                            "There is a Error in the Json, review that task"
                            " or penaltyText"
                            " and information is not empty"
                        ),
                        "error": "Bad Request",
                    }
                ),
                mimetype="application/json",
                status_code=500,
            )
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
            json.dumps({"cause": str(e), "error": "Internal Server Error"}),
            mimetype="application/json",
            status_code=500,
        )
