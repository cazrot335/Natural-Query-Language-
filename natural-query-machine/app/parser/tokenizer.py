import re


def tokenize(query):

    query = query.lower().strip()

    tokens = re.findall(
        r'\d+(?:\.\d+)?|[a-zA-Z_]+|[><=]',
        query
    )

    return tokens