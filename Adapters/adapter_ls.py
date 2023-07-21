import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction


def main(article: str) -> str:
    """
    summarize the text when the text is too long.
    Args: article: String with the text.
    returns: summary of the text
    """

    loaded_parameters = load_parameters()
    max_sentence_count = loaded_parameters[
        "language_studio"]["max_sentence_count"]
    client = authenticate_client()

    document = [article]

    poller = client.begin_analyze_actions(
        document,
        actions=[ExtractSummaryAction(max_sentence_count=max_sentence_count)],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]
        if extract_summary_result.is_error:
            print(
                "...Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                )
            )
        else:
            result = " ".join(
                [sentence.text for sentence in
                 extract_summary_result.sentences]
            )
            logging.warning(
                "Summary extracted: \n{}".format(
                    " ".join(
                        [sentence.text for sentence in
                         extract_summary_result.sentences]
                    )
                )
            )
    return result


def authenticate_client():
    key = os.environ["LSKEY"]
    endpoint = os.environ["LSENDPOINT"]
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=ta_credential
    )
    return text_analytics_client
