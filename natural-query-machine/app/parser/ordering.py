import re


def detect_ordering(query):

    query_lower = query.lower()

    pattern = (
        r'(?:ordered|sort|sorted)\s+by\s+'
        r'([a-zA-Z_ ]+?)'
        r'(?:\s+(ascending|descending|asc|desc))?'
        r'(?:\s|$)'
    )

    match = re.search(
        pattern,
        query_lower
    )

    if not match:

        return None

    field = match.group(1).strip()

    direction = match.group(2)

    if direction in [
        "descending",
        "desc"
    ]:

        direction = "DESC"

    else:

        direction = "ASC"

    return {
        "field": field,
        "direction": direction
    }