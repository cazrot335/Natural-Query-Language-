import re

from query.models import SCHEMA


FIELD_ALIASES = {

    # --------------------------------
    # Rentals
    # --------------------------------

    "car model": "car_model",
    "model": "car_model",

    "daily rate": "daily_rate",
    "rate": "daily_rate",

    "customer name": "customer_name",

    "rental date": "rental_date",
    "return date": "return_date",

    # --------------------------------
    # Students
    # --------------------------------

    "student name": "name",
    "student age": "age",
    "student marks": "marks",

    # --------------------------------
    # Teachers
    # --------------------------------

    "teacher name": "name",
    "teacher age": "age",

    # --------------------------------
    # Courses
    # --------------------------------

    "course name": "course_name"
}


CONDITION_OPERATORS = sorted(
    [
        "greater than",
        "more than",
        "above",
        "over",
        "less than",
        "lower than",
        "below",
        "under",
        "equal to",
        "equals",
        "equal"
    ],
    key=len,
    reverse=True
)


ORDER_PHRASES = [
    "ordered by",
    "order by",
    "sorted by",
    "sort by"
]


def detect_fields(query, table):

    query_lower = query.lower()

    available_fields = SCHEMA.get(
        table,
        []
    )

    occurrences = []

    # --------------------------------
    # Find field occurrences
    # --------------------------------

    for field in available_fields:

        readable_field = field.replace(
            "_",
            " "
        )

        search_terms = [
            field,
            readable_field
        ]

        # Add aliases
        for alias, alias_field in FIELD_ALIASES.items():

            if alias_field == field:

                search_terms.append(alias)

        for term in set(search_terms):

            pattern = rf"\b{re.escape(term)}\b"

            for match in re.finditer(
                pattern,
                query_lower
            ):

                occurrences.append({
                    "field": field,
                    "position": match.start(),
                    "end": match.end()
                })

    # --------------------------------
    # Sort fields by appearance
    # --------------------------------

    occurrences.sort(
        key=lambda item: item["position"]
    )

    # --------------------------------
    # Identify fields used in
    # conditions
    # --------------------------------

    condition_positions = set()

    for occurrence in occurrences:

        field_end = occurrence["end"]

        text_after = query_lower[
            field_end:
        ]

        for operator in CONDITION_OPERATORS:

            pattern = (
                rf"^\s+"
                rf"{re.escape(operator)}"
                rf"\s+"
                rf"\d+(?:\.\d+)?"
            )

            if re.match(
                pattern,
                text_after
            ):

                condition_positions.add(
                    occurrence["position"]
                )

                break

    # --------------------------------
    # Identify fields used in ORDER BY
    # --------------------------------

    order_positions = set()

    for occurrence in occurrences:

        field_position = occurrence[
            "position"
        ]

        for phrase in ORDER_PHRASES:

            order_position = query_lower.find(
                phrase
            )

            if order_position == -1:
                continue

            # Field is part of ORDER BY if
            # it occurs after "ordered by",
            # "sorted by", etc.

            if field_position > order_position:

                order_positions.add(
                    field_position
                )

    # --------------------------------
    # Build selected fields
    # --------------------------------

    selected_fields = []

    for occurrence in occurrences:

        position = occurrence[
            "position"
        ]

        field = occurrence[
            "field"
        ]

        # Skip condition fields
        if position in condition_positions:

            continue

        # Skip ORDER BY fields
        if position in order_positions:

            continue

        # Prevent duplicates
        if field not in selected_fields:

            selected_fields.append(
                field
            )

    return selected_fields