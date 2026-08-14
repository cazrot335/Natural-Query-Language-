def detect_intent(tokens):

    if "show" in tokens:
        return "SELECT"

    if "find" in tokens:
        return "SELECT"

    if "list" in tokens:
        return "SELECT"

    if "how" in tokens and "many" in tokens:
        return "COUNT"

    return "UNKNOWN"