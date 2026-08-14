ENTITIES = {
    "students": "students",
    "student": "students",
    "teachers": "teachers",
    "teacher": "teachers",
    "courses": "courses",
    "course": "courses"
}


def detect_entity(tokens):

    for token in tokens:
        if token in ENTITIES:
            return ENTITIES[token]

    return None