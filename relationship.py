class Relationship():
    def __init__(self, dominant, submissive, initiated_by):
        self.dominant = dominant
        self.submissive = submissive
        self.initiated_by = initiated_by
        self.pending = True


class Relationship_Handler():
    def __init__(self, bot):
        self.bot = bot

    async def handle_submit_query(self):
        print("Someone wants to submit.")

    async def handle_dominate_query(self):
        print("Someone wants to dominate.")