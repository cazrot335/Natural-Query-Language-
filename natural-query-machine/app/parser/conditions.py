import re


OPERATORS = {
    "greater than": ">",
    "more than": ">",
    "above": ">",
    "over": ">",

    "less than": "<",
    "lower than": "<",
    "below": "<",
    "under": "<",

    "equal to": "=",
    "equals": "=",
    "equal": "="
}


def detect_conditions(query, valid_fields):

    query_lower = query.lower()

    conditions = []

    # --------------------------------
    # Check every valid field against
    # every supported operator.
    # --------------------------------

    for field in valid_fields:

        readable_field = field.replace(
            "_",
            " "
        )

        for operator_text, operator_symbol in OPERATORS.items():

            pattern = (
                rf"\b{re.escape(readable_field)}\b"
                rf"\s+"
                rf"{re.escape(operator_text)}"
                rf"\s+"
                rf"(\d+(?:\.\d+)?)"
            )

            matches = re.finditer(
                pattern,
                query_lower
            )

            for match in matches:

                value = match.group(1)

                condition = {
                    "field": field,
                    "operator": operator_symbol,
                    "value": convert_value(value),
                    "_position": match.start()
                }

                conditions.append(condition)

    # --------------------------------
    # Sort conditions according to
    # their position in the query.
    # --------------------------------

    conditions.sort(
        key=lambda condition: condition["_position"]
    )

    # --------------------------------
    # Remove internal position data.
    # --------------------------------

    for condition in conditions:

        del condition["_position"]

    return conditions


def convert_value(value):

    if "." in value:

        return float(value)

    return int(value)