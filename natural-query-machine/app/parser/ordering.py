import re

from query.models import SCHEMA
from parser.fields import FIELD_ALIASES


ORDER_WORDS = [
    "ordered by",
    "order by",
    "sorted by",
    "sort by"
]


DIRECTIONS = {
    "ascending": "ASC",
    "ascending order": "ASC",
    "asc": "ASC",

    "descending": "DESC",
    "descending order": "DESC",
    "desc": "DESC"
}


def detect_ordering(query, table):

    query_lower = query.lower()

    valid_fields = SCHEMA.get(
        table,
        []
    )

    # --------------------------------
    # Find ordering phrase
    # --------------------------------

    order_position = -1
    order_phrase = None

    for phrase in ORDER_WORDS:

        position = query_lower.find(
            phrase
        )

        if position != -1:

            if (
                order_position == -1
                or position < order_position
            ):

                order_position = position
                order_phrase = phrase

    if order_phrase is None:

        return None

    # --------------------------------
    # Get text after "ordered by"
    # --------------------------------

    text_after = query_lower[
        order_position
        + len(order_phrase):
    ].strip()

    # --------------------------------
    # Find direction
    # --------------------------------

    direction = "ASC"

    for direction_text, sql_direction in DIRECTIONS.items():

        if re.search(
            rf"\b{re.escape(direction_text)}\b",
            text_after
        ):

            direction = sql_direction

            text_after = re.sub(
                rf"\b{re.escape(direction_text)}\b",
                "",
                text_after
            ).strip()

            break

    # --------------------------------
    # Find the field
    # --------------------------------

    field = find_order_field(
        text_after,
        valid_fields
    )

    if field is None:

        return None

    return {
        "field": field,
        "direction": direction
    }


def find_order_field(
    text,
    valid_fields
):

    candidates = []

    # --------------------------------
    # Check aliases
    # --------------------------------

    for alias, field in FIELD_ALIASES.items():

        if field not in valid_fields:
            continue

        position = text.find(
            alias
        )

        if position != -1:

            candidates.append({
                "field": field,
                "position": position,
                "length": len(alias)
            })

    # --------------------------------
    # Check schema fields
    # --------------------------------

    for field in valid_fields:

        readable_field = field.replace(
            "_",
            " "
        )

        for term in [
            field,
            readable_field
        ]:

            position = text.find(
                term
            )

            if position != -1:

                candidates.append({
                    "field": field,
                    "position": position,
                    "length": len(term)
                })

    if not candidates:

        return None

    # Prefer the field that appears first.
    # If positions are equal, prefer the
    # longer phrase.

    candidates.sort(
        key=lambda item: (
            item["position"],
            -item["length"]
        )
    )

    return candidates[0]["field"]