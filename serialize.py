from data_classes import Identity

def lexicon_to_string(lexicon: list) -> str:
    print("Converting lexicon to string.")
    reply = ""
    for word in lexicon:
        reply += word + ","
    reply = reply[:-1] #Remove dangling comma.
    return reply

def string_to_lexicon(string: str) -> list:
    return string.split(",")

def result_to_identity(result: list) -> Identity:
    print("Serializing result set to identity object")
    #Result will be a singleton list of tuples.
    #Get the first item.
    for display_name, lexicon in result:
        return Identity(display_name = display_name, lexicon = lexicon)

