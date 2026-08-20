def generate_sql(parsed_query):

    intent = parsed_query["intent"]

    table = parsed_query["table"]

    fields = parsed_query["fields"]

    conditions = parsed_query["conditions"]

    condition_tree = parsed_query.get(
        "condition_tree"
    )

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

    if condition_tree:

        where_clause = generate_condition_sql(
            condition_tree
        )

        sql += (
            " WHERE "
            + where_clause
        )

    elif conditions:

        # --------------------------------
        # Backward compatibility
        # --------------------------------

        condition_parts = []

        for index, condition in enumerate(
            conditions
        ):

            field = condition["field"]

            operator = condition["operator"]

            value = condition["value"]

            condition_sql = (
                f"{field} "
                f"{operator} "
                f"{value}"
            )

            if index == 0:

                condition_parts.append(
                    condition_sql
                )

            else:

                connector = condition.get(
                    "connector",
                    "AND"
                )

                condition_parts.append(
                    f"{connector} "
                    f"{condition_sql}"
                )

        sql += (
            " WHERE "
            + " ".join(
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


def generate_condition_sql(node):

    # --------------------------------
    # CONDITION node
    # --------------------------------

    if node["type"] == "CONDITION":

        condition = node["condition"]

        field = condition["field"]

        operator = condition["operator"]

        value = condition["value"]

        return (
            f"{field} "
            f"{operator} "
            f"{value}"
        )

    # --------------------------------
    # AND / OR node
    # --------------------------------

    if node["type"] in (
        "AND",
        "OR"
    ):

        left = generate_condition_sql(
            node["left"]
        )

        right = generate_condition_sql(
            node["right"]
        )

        operator = node["type"]

        # --------------------------------
        # Parentheses
        # --------------------------------

        return (
            f"({left} "
            f"{operator} "
            f"{right})"
        )

    raise ValueError(
        f"Unknown condition node: "
        f"{node['type']}"
    )