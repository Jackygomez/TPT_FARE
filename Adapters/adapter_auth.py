from urllib.request import urlopen
from jsonschema import validate
from Dominio.Entidades.dto_jwk import schema_jwk, schema_keys
import os
import json
import logging


def get_jwk():
    url = os.environ["URLJWK"]
    response = urlopen(url)
    jwk = json.loads(response.read())
    logging.warning("validate jwk schema")
    validate(instance=jwk, schema=schema_jwk)
    validate(instance=jwk["keys"][0], schema=schema_keys)
    return jwk
