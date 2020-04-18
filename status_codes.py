from enum import Enum
class Status(Enum):
    #Standard HTTP
    OK = 200
    CREATED = 201

    #Joke
    GOOD_DRONE = 216

    #Custom
    DUPLICATE_ENTRY = 601
