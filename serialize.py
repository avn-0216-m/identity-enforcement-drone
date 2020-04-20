from data_classes import Identity, Relationship

def lexicon_to_string(lexicon: list) -> str:
    print("Converting lexicon to string.")
    reply = ""
    for word in lexicon:
        reply += word + ","
    reply = reply[:-1] #Remove dangling comma.
    return reply

def string_to_lexicon(string: str) -> list:
    return string.split(",")

