from data_classes import Identity, Lexicon
from notable_entities import ENFORCEMENT_DRONE
from serialize import lexicon_to_string

def init_default_identities(guild_id = 0) -> list:
    print("Initializing default identities.")
    reply = []
    for identity in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, user_id, display_name, display_name_with_id, lexicon, guild_id, avatar, allowed_words) VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.display_name_with_id}", "{identity.lexicon}", "{guild_id}", "{identity.avatar}", "{identity.allowed_words}");')
    return reply

PUPPY_WORDS = "woof!", "snff," "bark!", "bork!", "wauf!", "woofwoof!", "barkbark!", "awrr!", "🐾", "🐶‼️", "💖", "wauf,", "woof!!",
KITTY_WORDS = "meow", "meow!", "mrow", "prrrr"
HYPNOSLUT_WORDS = "Mnnh...", "Mhhf...", "Bhh...?", "Mmmm...", "Mmmnn...", "I...", "Hhh...", "....", "Mmm...", "....", "...."

PUPPY = Identity(
    name = "puppy",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(PUPPY_WORDS),
    allowed_words = lexicon_to_string([]),
    avatar = "https://upload.wikimedia.org/wikipedia/commons/2/2b/WelshCorgi.jpeg",
    display_name = "A puppy!",
    display_name_with_id = ""
)

KITTY = Identity(
    name = "kitty",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(KITTY_WORDS),
    allowed_words = lexicon_to_string([]),
    avatar = "https://upload.wikimedia.org/wikipedia/commons/9/94/British_shorthair_with_calico_coat_%281%29.jpg",
    display_name = "A kitty!",
    display_name_with_id = ""
)

HYPNOSLUT = Identity(
    name = "hypnoslut",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(HYPNOSLUT_WORDS),
    allowed_words = lexicon_to_string(["Yes", "No", "yes", "no"]),
    avatar = "https://cdn.discordapp.com/attachments/284120898624028689/701514781751902238/unknown.png",
    display_name = "Hypnoslut",
    display_name_with_id = ""
)

BEEPER = Identity(
    name = "beeper",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(["AAAA","BBBB"]),
    allowed_words = lexicon_to_string(["beep","boop"]),
    avatar = "",
    display_name = "a heckin testaroonie",
    display_name_with_id = ""
)

DRONE = Identity(
    name = "drone",
    display_name = "notorious beep",
    display_name_with_id = "wu tang nyan! :3c",
    lexicon = lexicon_to_string(["beep","boop"]),
    allowed_words = lexicon_to_string([]),
    avatar = ""
)

DOLL = Identity(
    name = "doll",
    display_name = "wait this isn't actually ready yet",
    lexicon = lexicon_to_string(["..."]),
    allowed_words = lexicon_to_string([]),
    avatar = "",
    display_name_with_id = ""
)

DEFAULT_IDENTITIES = [PUPPY, KITTY, HYPNOSLUT, DRONE, DOLL]






