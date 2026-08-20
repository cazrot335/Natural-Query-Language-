from parser.intent import detect_intent
from parser.entities import detect_entity
from parser.fields import detect_fields
from parser.conditions import detect_conditions
from parser.ordering import detect_ordering
from parser.limit import detect_limit
from parser.boolean import build_condition_tree

from query.models import SCHEMA
from query.validator import validate_query
from query.sql_generator import generate_sql


def parse_query(query):

    # -----------------------------
    # Tokenize
    # -----------------------------

    tokens = query.lower().split()

    # -----------------------------
    # Detect intent
    # -----------------------------

    intent = detect_intent(tokens)

    # -----------------------------
    # Detect table
    # -----------------------------

    table = detect_entity(query)

    # -----------------------------
    # Detect fields
    # -----------------------------

    fields = []

    if table:

        fields = detect_fields(
            query,
            table
        )

    # -----------------------------
    # Get valid fields
    # -----------------------------

    valid_fields = []

    if table:

        valid_fields = SCHEMA[
            table
        ]

    # -----------------------------
    # Detect conditions
    # -----------------------------

    conditions = detect_conditions(
        query,
        valid_fields
    )

    # -----------------------------
# Build condition tree
# -----------------------------

    condition_tree = build_condition_tree(
        conditions
    )

    # -----------------------------
    # Detect ordering
    # -----------------------------

    order_by = detect_ordering(query, table)

    # -----------------------------
    # Detect limit
    # -----------------------------

    limit = detect_limit(
        query
    )

    # -----------------------------
    # Build structured query
    # -----------------------------

    return {

    "intent": intent,

    "table": table,

    "fields": fields,

    "conditions": conditions,

    "condition_tree": condition_tree,

    "order_by": order_by,

    "limit": limit
}


if __name__ == "__main__":

    query = input(
        "Enter query: "
    )

    try:

        parsed_query = parse_query(
            query
        )

        print(
            "\nStructured Query:"
        )

        print(parsed_query)

        # -----------------------------
        # Validate
        # -----------------------------

        validate_query(
            parsed_query
        )

        # -----------------------------
        # Generate SQL
        # -----------------------------

        sql = generate_sql(
            parsed_query
        )

        print(
            "\nGenerated SQL:"
        )

        print(sql)

    except ValueError as error:

        print(
            "\nError:"
        )

        print(error)