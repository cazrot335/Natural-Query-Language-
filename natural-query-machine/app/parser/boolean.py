def build_condition_tree(conditions):

    if not conditions:
        return None

    # --------------------------------
    # Convert conditions into tokens
    # --------------------------------

    expressions = []

    for index, condition in enumerate(
        conditions
    ):

        expressions.append({
            "type": "CONDITION",
            "condition": condition
        })

    # --------------------------------
    # Handle AND first
    # --------------------------------

    and_groups = []

    current_group = [
        expressions[0]
    ]

    for index in range(
        1,
        len(expressions)
    ):

        connector = conditions[index].get(
            "connector",
            "AND"
        )

        if connector == "AND":

            current_group.append(
                expressions[index]
            )

        else:

            and_groups.append(
                build_and_group(
                    current_group
                )
            )

            current_group = [
                expressions[index]
            ]

    and_groups.append(
        build_and_group(
            current_group
        )
    )

    # --------------------------------
    # Combine groups with OR
    # --------------------------------

    expression = and_groups[0]

    for group in and_groups[1:]:

        expression = {
            "type": "OR",
            "left": expression,
            "right": group
        }

    return expression


def build_and_group(expressions):

    expression = expressions[0]

    for right in expressions[1:]:

        expression = {
            "type": "AND",
            "left": expression,
            "right": right
        }

    return expression