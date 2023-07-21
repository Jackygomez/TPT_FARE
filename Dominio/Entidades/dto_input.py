schema_input = {
    "type": "object",
    "properties": {
        "task": {"type": "string"},
        "information": {"type": "object"},
        "penaltyText": {"type": "array"},
    },
    "required": [
        "task",
        "information",
        "penaltyText",
    ],
}

schema_information = {
    "type": "object",
    "properties": {
        "departureDate": {"type": "string"},
        "passengerChild": {"type": "array"},
    },
    "required": ["departureDate", "passengerChild"],
}

schema_passengerChild = {
    "type": "object",
    "properties": {
        "age": {"type": "integer"},
        "seat": {"type": "boolean"},
        "isAccompanied": {"type": "boolean"},
    },
    "required": ["age", "seat", "isAccompanied"],
}


schema_categories = {
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "freeText": {"type": "string"},
        "name": {"type": "string"},
    },
    "required": ["code", "freeText", "name"],
}


schemma_penaltyText = {
    "type": "object",
    "properties": {
        "fareBasis": {"type": "string"},
        "categories": {"type": "array"},
        "passengerTypes": {"type": "array"},
    },
    "required": ["fareBasis", "categories", "passengerTypes"],
}
