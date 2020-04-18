DATABASE_NAME = 'enforcement_drone'

MESSAGES = 'messages'
RELATIONSHIPS = 'relationships'

MIGRATION = [
    "DROP DATABASE enforcement_drone",
    "CREATE DATABASE enforcement_drone",
    "USE enforcement_drone",
    "CREATE TABLE messages(message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, discord_user_id BIGINT NOT NULL, message_content VARCHAR(255) NOT NULL);",
    "CREATE TABLE relationships(relationship_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, dominant_id BIGINT NOT NULL, submissive_id BIGINT NOT NULL, initiated_by BIGINT NOT NULL, pending BOOL);"
]