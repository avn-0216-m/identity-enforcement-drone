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

def result_to_identity(results: list) -> list: #Of identities:
    print(results)
    print("Serializing result set to identity object")
    reply = []
    for result in results:
        identity = Identity()
        try:
            identity.display_name = result["display_name"]
        except KeyError:
            pass
        try:
            identity.avatar = result["avatar"]
        except KeyError:
            pass
        try:
            identity.name = result["name"]
        except KeyError:
            pass
        reply.append(identity)
    return reply

