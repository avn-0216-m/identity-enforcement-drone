from database import Database_Handler
from data_classes import Relationship, Status, Response

class Relationship_Handler():
    def __init__(self, db):
        self.db = db

    def handle_submit_query(self) -> bool:
        print("Someone wants to submit.")

    def handle_submit_query(self, submissive, dominant) -> Response:
        results = self.db.find_potential_relationship(dominant.id, submissive.id).data
        print("Results are")
        print(results)
        if results == []:
            print("No duplicate results found. Continuing.")
            pass
        else:
            for result in results:
                if result.initiated_by == result.dominant_id and result.pending == 1:
                    self.db.confirm_relationship(result.relationship_id)
                    return Status.HOLY_MATRIHORNY
                else:
                    return Status.DUPLICATE_REQUEST
        return self.db.add_relationship(Relationship(dominant_id = dominant.id, submissive_id = submissive.id, initiated_by = submissive.id))

    def handle_dominate_query(self, dominant: discord.Member, submissive: discord.Member) -> Response:

        current_relationship = self.db.get_relationship(dominant.id, submissive.id).data

        if current_relationship is None:
            #Register the request in the DB.
            self.db.add_relationship(Relationship(dominant_id = dominant.id, submissive_id = submissive.id, initiated_by = dominant.id))
            return Status.CREATED
        elif current_relationship.pending == 1 and current_relationship.initiated_by == submissive.id:
            #Confirm the relationship.
            self.db_confirm_relationship(current_relationship.relationship_id)
            return Status.HOLY_MATRIHORNY
        else:
            #Disregard the duplicate request.
            return Status.DUPLICATE_REQUEST


        return 
