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


def detect_fields(query, table):

    query_lower = query.lower()

    available_fields = SCHEMA.get(
        table,
        []
    )

    # --------------------------------
    # Find all occurrences of fields
    # --------------------------------

    occurrences = []

    for field in available_fields:

        readable_field = field.replace(
            "_",
            " "
        )

        # Search both:
        #
        # daily_rate
        #
        # daily rate

        search_terms = [
            readable_field,
            field
        ]

        # Add aliases belonging to this field
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
    # Sort by position in user's query
    # --------------------------------

    occurrences.sort(
        key=lambda item: item["position"]
    )

    # --------------------------------
    # Find occurrences that are part
    # of conditions.
    # --------------------------------

    condition_occurrences = set()

    for occurrence in occurrences:

        field = occurrence["field"]

        readable_field = field.replace(
            "_",
            " "
        )

        field_end = occurrence["end"]

        text_after_field = query_lower[
            field_end:
        ]

        # Only inspect a short portion
        # after the field.
        #
        # Example:
        #
        # daily rate above 500
        #
        # This should be a condition.

        for operator in CONDITION_OPERATORS:

            pattern = (
                rf"^\s+"
                rf"{re.escape(operator)}"
                rf"\s+"
                rf"\d+(?:\.\d+)?"
            )

            if re.match(
                pattern,
                text_after_field
            ):

                condition_occurrences.add(
                    occurrence["position"]
                )

                break

    # --------------------------------
    # Build selected fields.
    # --------------------------------

    selected_fields = []

    for occurrence in occurrences:

        position = occurrence["position"]

        field = occurrence["field"]

        # Skip field occurrence if it is
        # being used as a condition.

        if position in condition_occurrences:

            continue

        if field not in selected_fields:

            selected_fields.append(field)

    return selected_fields