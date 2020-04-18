from enum import Enum

class Relationship():
    def __init__(self, dominant, submissive, initiated_by):
        self.dominant = dominant
        self.submissive = submissive
        self.initiated_by = initiated_by
        self.pending = True

class Identity():
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.server = None
        self.lexicon = None
        self.allowed_words = None
        self.avatar = None

class Subject():
    def __init__(self):
        self.discord_id = None
        self.drone_id = None
        self.safe_words = None

class Status(Enum):
    #Standard HTTP
    OK = 200
    CREATED = 201

    #Joke
    GOOD_DRONE = 216

    #Custom
    DUPLICATE_ENTRY = 601

class Response():
    def __init__(self, status: Status, data = None):
        self.status = status
        self.data = data