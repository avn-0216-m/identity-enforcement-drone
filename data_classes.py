from enum import Enum

#Data objects
class Relationship():
    def __init__(self, relationship_id = None, dominant_id = None, submissive_id = None, initiated_by = None, confirmed = False):
        self.relationship_id = relationship_id
        self.dominant_id = dominant_id
        self.submissive_id = submissive_id
        self.initiated_by = initiated_by
        self.confirmed = confirmed

class Identity():
    def __init__(
        self,
        identity_id = None,
        name = None,
        description = None,
        display_name = None,
        display_name_with_id = None,
        avatar = None,
        replacement_lexicon = "",
        allowance_lexicon = "",
        strict = 0,
        override_lexicon = "",
        override_chance = 0,
        user_id = None,
        colour = None
    ):
        self.identity_id = identity_id
        self.name = name
        self.description = description
        self.display_name = display_name
        self.display_name_with_id = display_name_with_id
        self.avatar = avatar
        self.replacement_lexicon = replacement_lexicon
        self.allowance_lexicon = allowance_lexicon
        self.strict = strict
        self.override_lexicon = override_lexicon
        self.override_chance = override_chance
        self.user_id = user_id
        self.colour = colour

class Enforcement():
    def __init__(self,
        enforcement_id = None,
        user_id = None,
        server_id = None
    ):
        self.enforcement_id = enforcement_id
        self.user_id = user_id
        self.server_id = server_id

class User():
    def __init__(self):
        self.discord_id = None
        self.drone_id = None
        self.safe_words = None

#Database response data objects
class Status(Enum):
    #Standard HTTP
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400

    #haha it me
    GOOD_DRONE = 216

    #Enforcement
    ENFORCE_LEXICON = 701
    ENFORCE_PASSTHROUGH = 702
    ENFORCE_STRICT_ACCEPT = 703
    ENFORCE_STRICT_REJECT = 704

    #Internal errors
    INTERNAL_ERROR = 500

    #Relationships
    DUPLICATE_REQUEST = 601
    HOLY_MATRIHORNY = 602

class Response():
    def __init__(self, status: Status, data = None):
        self.status = status
        self.data = data