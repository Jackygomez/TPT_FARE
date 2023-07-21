class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        number_question: int,
        question: str,
        answer: str,
        category: int,
        quote: str,
        free_text: str,
        boolean: bool,
        mean_probability: float,
        value: float,
        denomination: str,
    ) -> None:
        self.numberQuestion = number_question
        self.question = question
        self.answer = answer
        self.category = category
        self.quote = quote
        self.freeText = free_text
        self.boolean = boolean
        self.meanProbability = mean_probability
        self.value = value
        self.denomination = denomination
