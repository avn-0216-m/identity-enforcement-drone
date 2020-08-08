from data_classes import Identity, Relationship
from notable_entities import SERIALIZER_DIVIDER

def lexicon_to_string(lexicon: list) -> str:
    if lexicon is None:
        return None
    reply = ""
    for word in lexicon:
        reply += word + SERIALIZER_DIVIDER
    reply = reply[:-1] #Remove dangling comma.
    return reply

def string_to_lexicon(string: str) -> list:
    return string.split(SERIALIZER_DIVIDER)

