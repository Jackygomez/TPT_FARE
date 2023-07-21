
schema_jwk = {
    "type": "object",
    "properties": {
        "keys": {"type": "array"},
    },
    "required": ["keys"],
}

schema_keys = {
    "type": "object",
    "properties": {
        "kty": {"type": "string"},
        "use": {"type": "string"},
        "kid": {"type": "string"},
        "x5t": {"type": "string"},
        "e": {"type": "string"},
        "n": {"type": "string"},
        "x5c": {"type": "array"},
        "alg": {"type": "string"},
    },
    "required": ["kty", "use", "kid", "x5t", "e", "n", "x5c", "alg"],
}
