from query.models import SCHEMA


def validate_query(parsed_query):

    table = parsed_query["table"]

    # -----------------------------
    # Validate table
    # -----------------------------

    if table not in SCHEMA:

        raise ValueError(
            f"Unknown table: {table}"
        )

    valid_fields = SCHEMA[table]

    # -----------------------------
    # Validate SELECT fields
    # -----------------------------

    for field in parsed_query["fields"]:

        if field not in valid_fields:

            raise ValueError(
                f"Unknown field '{field}' "
                f"for table '{table}'"
            )

    # -----------------------------
    # Validate conditions
    # -----------------------------

    for condition in parsed_query["conditions"]:

        field = condition["field"]

        if field not in valid_fields:

            raise ValueError(
                f"Unknown condition field "
                f"'{field}'"
            )

    # -----------------------------
    # Validate ORDER BY
    # -----------------------------

    if parsed_query["order_by"]:

        field = parsed_query[
            "order_by"
        ]["field"]

        if field not in valid_fields:

            raise ValueError(
                f"Unknown ORDER BY field "
                f"'{field}'"
            )

    return True