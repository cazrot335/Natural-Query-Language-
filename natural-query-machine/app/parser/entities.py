from query.models import SCHEMA


ENTITY_ALIASES = {
    "student": "students",
    "students": "students",

    "teacher": "teachers",
    "teachers": "teachers",

    "course": "courses",
    "courses": "courses",

    "rental": "rentals",
    "rentals": "rentals",

    "rental record": "rentals",
    "rental records": "rentals"
}


def detect_entity(query):

    query_lower = query.lower()

    # --------------------------------
    # 1. Check explicit entity names
    # --------------------------------

    aliases = sorted(
        ENTITY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for phrase, table in aliases:

        if phrase in query_lower:

            return table

    # --------------------------------
    # 2. Check actual schema table names
    # --------------------------------

    for table in SCHEMA:

        if table.lower() in query_lower:

            return table

    # --------------------------------
    # 3. Infer table from fields
    # --------------------------------

    table_scores = {}

    for table, fields in SCHEMA.items():

        score = 0

        for field in fields:

            field_readable = field.replace(
                "_",
                " "
            )

            # Check database field name
            if field.lower() in query_lower:

                score += 1

            # Check human-readable field name
            elif field_readable.lower() in query_lower:

                score += 1

        if score > 0:

            table_scores[table] = score

    # --------------------------------
    # 4. Return highest scoring table
    # --------------------------------

    if table_scores:

        return max(
            table_scores,
            key=table_scores.get
        )

    return None