import re


OPERATORS = {
    # -----------------------------
    # Greater than
    # -----------------------------

    "greater than": ">",
    "more than": ">",
    "above": ">",
    "over": ">",
    "higher than": ">",
    "exceeding": ">",
    "exceeds": ">",

    # -----------------------------
    # Less than
    # -----------------------------

    "less than": "<",
    "lower than": "<",
    "below": "<",
    "under": "<",
    "fewer than": "<",
    "lower": "<",

    # -----------------------------
    # Equal
    # -----------------------------

    "equal to": "=",
    "equals": "=",
    "equal": "=",
    "is equal to": "=",
}


def detect_conditions(query, valid_fields):

    query_lower = query.lower()

    conditions = []

    # --------------------------------
    # Find all conditions
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

                    # Internal parser positions
                    "_position": match.start(),
                    "_end": match.end()
                }

                conditions.append(condition)

    # --------------------------------
    # Sort conditions by their position
    # in the original query
    # --------------------------------

    conditions.sort(
        key=lambda condition: condition["_position"]
    )

    # --------------------------------
    # Detect AND / OR between
    # conditions
    # --------------------------------

    for index in range(1, len(conditions)):

        previous = conditions[index - 1]
        current = conditions[index]

        between = query_lower[
            previous["_end"]:current["_position"]
        ]

        # Default connector
        connector = "AND"

        # Look for OR first
        if re.search(
            r"\bor\b",
            between
        ):

            connector = "OR"

        elif re.search(
            r"\band\b",
            between
        ):

            connector = "AND"

        current["connector"] = connector

    # --------------------------------
    # First condition has no connector
    # --------------------------------

    if conditions:

        conditions[0]["connector"] = None

    # --------------------------------
    # Remove internal parser data
    # --------------------------------

    for condition in conditions:

        del condition["_position"]
        del condition["_end"]

    return conditions


def convert_value(value):

    if "." in value:

        return float(value)

    return int(value)