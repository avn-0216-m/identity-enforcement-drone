class Relationship():
    def __init__(self, dominant, submissive, initiated_by):
        self.dominant = dominant
        self.submissive = submissive
        self.initiated_by = initiated_by
        self.pending = True

class Identity():
    def __init__(name, owner):
        self.name = name
        self.owner = owner
        self.server = None
        self.lexicon = None
        self.allowed_words = None
        self.avatar = None