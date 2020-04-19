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
        guild_id = None,
        lexicon_id = None,
        allowed_words = None,
        avatar = None,
        uses_drone_id = False,
        display_name = None,
        display_name_with_id = None 
    ):
        self.identity_id = identity_id
        self.name = name
        self.user_id = user_id
        self.guild_id = guild_id
        self.lexicon_id = lexicon_id
        self.allowed_words = allowed_words
        self.avatar = avatar
        self.uses_drone_id = uses_drone_id
        self.display_name = display_name
        self.display_name_with_id = display_name_with_id

class Subject():
    def __init__(self):
        self.discord_id = None
        self.drone_id = None
        self.safe_words = None

class Lexicon():
    def __init__(
        self,
        lexicon_id = None,
        word = None
    ):
        self.lexicon_id = lexicon_id
        self.word = word

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