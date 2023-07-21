class Respond:
    """This is a data transfer object for the response of the pipeline"""

    def __init__(
        self,
        fare_basis: list,
        passenger_types: list,
        model_respond: list,
        average: float,
        free_text: list,
    ) -> None:
        self.fareBasis = fare_basis
        self.passengerTypes = passenger_types
        self.modelRespond = model_respond
        self.average = average
        self.freeText = free_text
