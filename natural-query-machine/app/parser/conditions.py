OPERATORS = {
    "above": ">",
    "over": ">",
    "greater": ">",
    "below": "<",
    "under": "<",
    "less": "<",
    "equals": "=",
    "equal": "="
}


def detect_condition(tokens):

    for i, token in enumerate(tokens):

        if token in OPERATORS:

            operator = OPERATORS[token]

            if i + 1 < len(tokens):
                value = tokens[i + 1]

                field = None

                if i > 0:
                    field = tokens[i - 1]

                return {
                    "field": field,
                    "operator": operator,
                    "value": value
                }

    return None