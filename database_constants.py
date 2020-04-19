from default_identities import initialize_default_identities

DATABASE_NAME = 'enforcement_drone'

MESSAGES = 'messages'
RELATIONSHIPS = 'relationships'

def drop_database() -> list:
    return ["DROP DATABASE enforcement_drone",
    "CREATE DATABASE enforcement_drone",
    "USE enforcement_drone"]

def create_tables() -> list:
    return ["CREATE TABLE messages(message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL, message_content VARCHAR(255) NOT NULL);",
    "CREATE TABLE relationships(relationship_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, dominant_id BIGINT NOT NULL, submissive_id BIGINT NOT NULL, initiated_by BIGINT NOT NULL, pending BOOL);",
    "CREATE TABLE identities(identity_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, user_id BIGINT NOT NULL);"]

MIGRATION = drop_database() + create_tables() + initialize_default_identities()