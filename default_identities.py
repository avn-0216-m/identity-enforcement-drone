from data_classes import Identity, Lexicon
from notable_entities import ENFORCEMENT_DRONE

def init_default_identities(guild_id = 0) -> list:
    print("Initializing default identities.")
    reply = []
    for identity in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, user_id, display_name, lexicon_id, guild_id) VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.lexicon_id}", "{guild_id}");')
    return reply

PUPPY = Identity(
    name = "puppy",
    user_id = ENFORCEMENT_DRONE,
    allowed_words = [],
    lexicon = [PUPPY_WORDS],
    avatar = "https://upload.wikimedia.org/wikipedia/commons/2/2b/WelshCorgi.jpeg",
    display_name = "A puppy!",
)

KITTY = Identity(
    name = "kitty",
    user_id = ENFORCEMENT_DRONE,
    lexicon = [KITTY_WORDS]
    allowed_words = [],
    lexicon_id = 2,
    avatar = "",
    display_name = "A kitty!",
)

PUPPY_WORDS = "woof", "woof!", "bark!", "wauf"
KITTY_WORDS = "meow", "meow!", "mrow", "prrrr"

PUPPY_LEXICON = map_words_list_to_lexicon_list(PUPPY_WORDS, 1)
KITTY_LEXICON = map_words_list_to_lexicon_list(KITTY_WORDS, 2)

DEFAULT_LEXICONS = [PUPPY_LEXICON, KITTY_LEXICON]
DEFAULT_IDENTITIES = [PUPPY, KITTY]






