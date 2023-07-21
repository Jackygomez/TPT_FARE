def validate_error(respond: object) -> str:
    if "gpt_paragraph_text" in respond.output:
        cause = """It was dont found information
        about Cancellation or Change in the free_text."""
    elif "maximum context length" in respond.output:
        cause = "The length of the text is too long for the GPT-3 model."
    elif "APIConnectionError" in respond.output:
        cause = "There is not more credits for the GPT-3 model."
    elif "ActivitiesSortAnswerCancellation" in respond.output:
        cause = "GPT dont answer the question, check the tokens."
    elif "No questions in the category" in respond.output:
        cause = respond.output
    else:
        cause = "unknown"
    return cause
