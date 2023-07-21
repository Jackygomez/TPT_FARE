import os
import openai
import logging
import numpy as np

from tenacity import (
    retry,
    stop_after_attempt,
)

from Dominio.Servicios.load_parameter import load_parameters


@retry(stop=stop_after_attempt(os.environ["RETRYATTEMPTS"]))
def logic_retry_openai(**kwargs):
    """
    This is a function for retry openai.
    Args: kwargs
    Returns: response
    """
    return openai.Completion.create(**kwargs)


def login_openai() -> dict:
    """
    This is a function for  login to openai.
    """
    logging.warning("Executing login_openai")
    try:

        openai.api_key = os.environ["AZOPENAIKEY"]
        openai.api_base = os.environ["AZOPENAIENDPOINT"]
        openai.api_type = os.environ["AZOPENAITYPE"]
        openai.api_version = os.environ["AZOPENAIVERSION"]

    except Exception as e:
        print("No credentials for openai")
        print(e)


def ask_openai(text: str, task: str) -> dict:
    """
    This is a function for
    ask question to AZURE GPT by OpenAI.
    """
    logging.warning("Executing ask_openai")
    login_openai()
    loaded_parameters = load_parameters()
    parameters = loaded_parameters["open_ai_parameters_change"]
    prompt = parameters["prompt"]
    prompt = f"{prompt}:\n\n{text}"
    response = logic_retry_openai(
        engine=parameters["model"],
        prompt=prompt,
        temperature=parameters["temperature"],
        max_tokens=parameters["max_tokens"],
        top_p=parameters["top_p"],
        frequency_penalty=parameters["frequency_penalty"],
        presence_penalty=parameters["presence_penalty"],
        logprobs=1,
    )

    response_mean_probability = mean_probability(response)
    try:
        return {
            "text": response.choices[0].text.lstrip(),
            "meanProbability": response_mean_probability,
        }
    except Exception as e:
        logging.warning("Error in ask_openai")
        logging.warning(e)
        logging.warning(response.choices)


def mean_probability(response: object) -> float:
    """
    This is a function for
    calculate mean probability.
    """
    logging.warning("Executing mean_probability")
    list_probs = []
    list_top_logprobs = list(response.choices[0].logprobs.top_logprobs)
    for top_logprobs_object in list_top_logprobs:
        for key, logprob in top_logprobs_object.items():
            list_probs.append(np.e ** float(logprob))

    mean_probability = sum(list_probs) / len(list_probs) * 100

    return mean_probability
