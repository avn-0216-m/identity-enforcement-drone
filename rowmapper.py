from data_classes import Relationship, Identity, User

def result_to_identity(results: list) -> list: #Of identities:
    reply = []
    for result in results:
        identity = Identity()
        for key in result.keys():

            value = result[key]
            if value == "None":
                value = None
            setattr(identity, key, value)
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

def result_to_user(results: list) -> list: #Of users
    reply = []
    for result in results:
        user = User()
        for key in result.keys():
            setattr(user, key, result[key])
        reply.append(user)
    return reply    

