from data_classes import Relationship, Identity

def result_to_identity(results: list) -> list: #Of identities:
    reply = []
    for result in results:
        identity = Identity()
        for key in result.keys():
            setattr(identity, key, result[key])
        reply.append(identity)
    return reply

def result_to_relationship(results: list) -> list: #Of relationships
    reply = []
    for result in results:
        relationship = Relationship()
        for key in result.keys():
            setattr(relationship, key, result[key])
        reply.append(relationship)
    return reply

