def generate_sql(parsed_query):

    intent = parsed_query["intent"]

    table = parsed_query["table"]

    fields = parsed_query["fields"]

    conditions = parsed_query["conditions"]

    order_by = parsed_query["order_by"]

    limit = parsed_query["limit"]

    # --------------------------------
    # SELECT
    # --------------------------------

    if intent == "SELECT":

        if fields:

            select_clause = ", ".join(
                fields
            )

        else:

            select_clause = "*"

        sql = (
            f"SELECT {select_clause} "
            f"FROM {table}"
        )

    # --------------------------------
    # COUNT
    # --------------------------------

    elif intent == "COUNT":

        sql = (
            f"SELECT COUNT(*) "
            f"FROM {table}"
        )

    else:

        raise ValueError(
            "Unsupported intent."
        )

    # --------------------------------
    # WHERE
    # --------------------------------

    if conditions:

        condition_parts = []

        for condition in conditions:

            field = condition["field"]

            operator = condition["operator"]

            value = condition["value"]

            condition_parts.append(
                f"{field} "
                f"{operator} "
                f"{value}"
            )

        sql += (
            " WHERE "
            + " AND ".join(
                condition_parts
            )
        )

    # --------------------------------
    # ORDER BY
    # --------------------------------

    if order_by:

        sql += (
            f" ORDER BY "
            f"{order_by['field']} "
            f"{order_by['direction']}"
        )

    # --------------------------------
    # LIMIT
    # --------------------------------

    if limit:

        sql += f" LIMIT {limit}"

    sql += ";"

    return sql