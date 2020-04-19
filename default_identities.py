from data_classes import Identity, Lexicon
from notable_entities import ENFORCEMENT_DRONE
from serialize import lexicon_to_string

def init_default_identities(guild_id = 0) -> list:
    print("Initializing default identities.")
    reply = []
    for identity in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, user_id, display_name, lexicon, guild_id, avatar) VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.lexicon}", "{guild_id}", "{identity.avatar}");')
    return reply

PUPPY_WORDS = "woof", "woof!", "bark!", "wauf"
KITTY_WORDS = "meow", "meow!", "mrow", "prrrr"
HYPNOSLUT_WORDS = "Mnnh...", "Mhhf...", "Bhh...?", "I...", "Hhh...", "....", "Mmm..."

PUPPY = Identity(
    name = "puppy",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(PUPPY_WORDS),
    allowed_words = lexicon_to_string([]),
    avatar = "https://upload.wikimedia.org/wikipedia/commons/2/2b/WelshCorgi.jpeg",
    display_name = "A puppy!",
)

KITTY = Identity(
    name = "kitty",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(KITTY_WORDS),
    allowed_words = lexicon_to_string([]),
    avatar = "https://upload.wikimedia.org/wikipedia/commons/9/94/British_shorthair_with_calico_coat_%281%29.jpg",
    display_name = "A kitty!",
)

HYPNOSLUT = Identity(
    name = "hypnoslut",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(HYPNOSLUT_WORDS),
    allowed_words = lexicon_to_string(["Yes", "No"]),
    avatar = "",
    display_name = "Hypnoslut"
)

DEFAULT_IDENTITIES = [PUPPY, KITTY]






