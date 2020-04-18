from database import Database_Handler
from data_classes import Relationship

class Relationship_Handler():
    def __init__(self, db):
        self.db = db

    def handle_submit_query(self) -> bool:
        print("Someone wants to submit.")

    def handle_dominate_query(self) -> bool:
        print("Someone wants to dominate.")

        self.db.get_all_from_table()

        return self.db.add_relationship(Relationship("beep", "boop", "beep"))
    

