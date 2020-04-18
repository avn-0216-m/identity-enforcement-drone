from database import Database_Handler
from data_classes import Relationship, Status, Response

class Relationship_Handler():
    def __init__(self, db):
        self.db = db

    def handle_submit_query(self) -> bool:
        print("Someone wants to submit.")

    def handle_dominate_query(self, dominant, submissive) -> Response:
        print(dominant.display_name + " wants to dominate " + submissive.display_name)
        if self.db.find_prexisting_relationship(dominant.id, submissive.id, dominant.id):
            return Status.DUPLICATE_ENTRY
        print("No duplicate entries found, adding initial domination request to database.")
        if self.db.add_relationship(Relationship(dominant.id, submissive.id, dominant.id)) is Status.OK:
            return Response(Status.OK, self.db.get_number_of_submissives(dominant.id))
    

