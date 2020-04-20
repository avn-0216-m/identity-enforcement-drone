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
        try:
            identity.lexicon = result["lexicon"]
        except KeyError:
            pass
        try:
            identity.allowed_words = result["allowed_words"]
        except KeyError:
            pass
        reply.append(identity)
    return reply

def result_to_relationship(results: list) -> list: #Of relationships
    print("Serializing result set to list of relationships.")
    print("Results are:")
    print(results)
    reply = []
    for result in results:
        relationship = Relationship()
        try:
            relationship.relationship_id = result["relationship_id"]
        except KeyError:
            pass
        try:
            relationship.dominant_id = result["dominant_id"]
        except KeyError:
            pass
        try:
            relationship.submissive_id = result["submissive_id"]
        except KeyError:
            pass
        try:
            relationship.initiated_by = result["initiated_by"]
        except KeyError:
            pass
        try:
            relationship.pending = result["pending"]
        except KeyError:
            pass
        reply.append(relationship)
    print("Reply is:")
    print(reply)
    return reply

