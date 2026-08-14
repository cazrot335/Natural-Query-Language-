import re


def detect_limit(query):

    query_lower = query.lower()

    patterns = [

        r'\bfirst\s+(\d+)\b',

        r'\btop\s+(\d+)\b',

        r'\bonly\s+(\d+)\b',

        r'\bjust\s+(\d+)\b',

        r'\blimit\s+(\d+)\b'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query_lower
        )

        if match:

            return int(
                match.group(1)
            )

    return None