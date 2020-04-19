from default_identities import init_default_identities, init_default_lexicons

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
    "CREATE TABLE identities(identity_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, user_id BIGINT NOT NULL, lexicon_id INT, display_name VARCHAR(255), server_id BIGINT);",
    "CREATE TABLE lexicons(lexicon_id INT NOT NULL, word VARCHAR(255) NOT NULL);"]

def get_migration() -> list:
    return drop_database() + create_tables() + init_default_lexicons() + init_default_identities()