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
    display_name = "",
    display_name_with_id = "#{}"
)

KITTY = Identity(
    name = "kitty",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(KITTY_WORDS),
    allowed_words = lexicon_to_string([]),
    avatar = "https://upload.wikimedia.org/wikipedia/commons/9/94/British_shorthair_with_calico_coat_%281%29.jpg",
    display_name = "",
    display_name_with_id = "#{}"
)

HYPNOSLUT = Identity(
    name = "hypnoslut",
    user_id = ENFORCEMENT_DRONE,
    lexicon = lexicon_to_string(HYPNOSLUT_WORDS),
    allowed_words = lexicon_to_string(["Yes", "No", "yes", "no"]),
    avatar = "https://cdn.discordapp.com/attachments/284120898624028689/701514781751902238/unknown.png",
    display_name = "",
    display_name_with_id = "Hypnoslut #{}"
)

DRONE = Identity(
    name = "drone",
    user_id = ENFORCEMENT_DRONE,
    display_name = "A faceless, anonymous drone",
    display_name_with_id = "Drone #{}",
    lexicon = "",
    allowed_words = "",
    avatar = "https://images.squarespace-cdn.com/content/v1/5cd68fb28dfc8ce502f14199/1586799484353-XBXNJR1XBM84C9YJJ0RU/ke17ZwdGBToddI8pDm48kLxnK526YWAH1qleWz-y7AFZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVFUQAah1E2d0qOFNma4CJuw0VgyloEfPuSsyFRoaaKT76QvevUbj177dmcMs1F0H-0/Drone.png"
)

SPECIALDOLL = Identity(
    name = "realdoll",
    user_id = ENFORCEMENT_DRONE,
    display_name = "A collectible doll",
    lexicon = "",
    allowed_words = lexicon_to_string(["{} is a pretty doll and it loves to be displayed.", "{} is a pretty doll and it loves to be displayed"]),
    avatar = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/190707-index-madame-alexander-ii-1562606955.png",
    display_name_with_id = "Collectible doll #{}/9999"
)

SPECIALDRONE = Identity(
    name = "good_drone",
    user_id = ENFORCEMENT_DRONE,
    display_name = "Good little drone",
    lexicon = "",
    allowed_words = lexicon_to_string(["{} is a good drone and it loves to obey", "{} is a good drone and it loves to obey.", "It feels good to obey."]),
    avatar = "https://images.squarespace-cdn.com/content/v1/5cd68fb28dfc8ce502f14199/1586799484353-XBXNJR1XBM84C9YJJ0RU/ke17ZwdGBToddI8pDm48kLxnK526YWAH1qleWz-y7AFZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVFUQAah1E2d0qOFNma4CJuw0VgyloEfPuSsyFRoaaKT76QvevUbj177dmcMs1F0H-0/Drone.png",
    display_name_with_id = "Good little drone #{}~"
)

DEFAULT_IDENTITIES = [PUPPY, KITTY, HYPNOSLUT, DRONE, SPECIALDOLL, SPECIALDRONE]






