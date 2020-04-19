from enum import Enum

#Data objects
class Relationship():
    def __init__(self, dominant, submissive, initiated_by):
        self.dominant = dominant
        self.submissive = submissive
        self.initiated_by = initiated_by
        self.pending = 1

class Identity():
    def __init__(
        self,
        identity_id = None, 
        name = None, 
        user_id = None, 
        server = None,
        lexicon_id = None,
        allowed_words = None,
        avatar = None,
        uses_drone_id = False,
        display_name = None,
        display_name_with_id = None 
    ):
        self.identity_id = None
        self.name = name
        self.user_id = user_id
        self.server = None
        self.lexicon_id = None
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

#Database response data objects
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