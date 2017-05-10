schema = {
    "type" : "object",
    "properties": {
        "version": {"type": "number"},
        "metrics": {"type": "array",
            "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                        "unit": {"type": "string"},
                        "comment": {"type": "string"}
                    },
                    "required": ["name", "value", "unit"],
                    "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
    "required": ["version", "metrics"]
}
