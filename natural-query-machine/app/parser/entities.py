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

    # Check longer phrases first
    aliases = sorted(
        ENTITY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for phrase, table in aliases:

        if phrase in query_lower:
            return table

    # Fallback to schema table names
    for table in SCHEMA:

        if table in query_lower:
            return table

    return None