from enum import Enum

class Relationship():
    def __init__(self, dominant, submissive, initiated_by):
        self.dominant = dominant
        self.submissive = submissive
        self.initiated_by = initiated_by
        self.pending = 1

class Identity():
    def __init__(
        self, 
        name = None, 
        owner = None, 
        server = None,
        lexicon = None,
        allowed_words = None,
        avatar = None,
        uses_drone_id = False,
        display_name = None,
        display_name_with_id = None 
    ):
        self.name = name
        self.owner = owner
        self.server = None
        self.lexicon = None
        self.allowed_words = None
        self.avatar = None
        self.uses_drone_id = False
        self.display_name = None
        self.display_name_with_id = None

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
    DUPLICATE_REQUEST = 601

class Response():
    def __init__(self, status: Status, data = None):
        self.status = status
        self.data = data