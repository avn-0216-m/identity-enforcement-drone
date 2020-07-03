from data_classes import Relationship, Identity, User
import logging
logger = logging.getLogger('Identity Enforcement Drone')

def map_rows(rows, output_class):

    #fetchone() returns a single dictionary, whereas
    #fetchall() returns a list.
    #We need to account for it here.

    if rows is None: return None

    if type(rows) is dict:
        logger.info("Mapping one row.")
        dictionary = rows
        output_object = output_class()
        for key in dictionary:
            setattr(output_object, key, dictionary[key])
        return output_object

    else:
        logger.info("Mapping many rows.")
        reply = []
        for row in rows:
            output_object = output_class()
            for key in row:
                setattr(output_object, key, row[key])
            reply.append(output_object)
        logger.info(f"Returning {len(reply)} rows mapped as {output_class}")
        return reply
            
                

