from kedro.config import ConfigLoader, MissingConfigException


def load_parameters() -> dict:
    """
    Funtion for load parameters from /parameters.
    """

    conf_loader = ConfigLoader(conf_source="conf", env="local")

    try:
        parameters = conf_loader.get("parameters*", "parameters*/**")
    except MissingConfigException:
        parameters = {}

    return parameters
