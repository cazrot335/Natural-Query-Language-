from parser.tokenizer import tokenize
from parser.intent import detect_intent
from parser.entities import detect_entity
from parser.conditions import detect_condition


def parse_query(query):

    tokens = tokenize(query)

    intent = detect_intent(tokens)

    entity = detect_entity(tokens)

    condition = detect_condition(tokens)

    result = {
        "intent": intent,
        "entity": entity,
        "conditions": []
    }

    if condition:
        result["conditions"].append(condition)

    return result


if __name__ == "__main__":

    query = input("Enter query: ")

    result = parse_query(query)

    print(result)