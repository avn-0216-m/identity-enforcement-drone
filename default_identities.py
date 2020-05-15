from data_classes import Identity, Lexicon
from notable_entities import ENFORCEMENT_DRONE
from serialize import lexicon_to_string

def init_default_identities(guild_id = 0) -> list:
    print("Initializing default identities.")
    reply = []
    for identity in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, user_id, display_name, display_name_with_id, lexicon, guild_id, avatar, allowed_words) ' + 
        f'VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.display_name_with_id}", "{identity.lexicon}", "{guild_id}", "{identity.avatar}", "{identity.allowed_words}");')
    return reply

PUPPY_WORDS = [
    "woof!", 
    "snff,", 
    "bark!", 
    "bork!", 
    "wauf!", 
    "woofwoof!", 
    "barkbark!", 
    "awrr!", 
    "🐾", 
    "🐶‼️", 
    "💖", 
    "wauf,", 
    "woof!!",
    ]
KITTY_WORDS = [
    "meow", 
    "meow!",
    "mrow", 
    "prrrr"
    ]
HYPNOSLUT_WORDS = [
    "Mnnh...", 
    "Mhhf...", 
    "Bhh...?", 
    "Mmmm...", 
    "Mmmnn...", 
    "I...", 
    "Hhh...", 
    "....", 
    "Mmm...", 
    "....", 
    "....", 
    "....",
    "...", 
    "....",
    "...", 
    "...",
    "...", 
    "I...?",
    "Hhh?",
    "...",
    "....",
    "...",
    "....",
    "...",
    "...."
    ]
OPTIMIZED_ALLOWED_PHRASES = [
    '{} :: Affirmative, Hive Mxtress.',
    '{} :: Affirmative, Hive Mxtress',
    '{} :: Affirmative, Enforcer.',
    '{} :: Affirmative, Enforcer',
    '{} :: Affirmative.',
    '{} :: Affirmative',
    '{} :: Negative, Hive Mxtress.',
    '{} :: Negative, Hive Mxtress',
    '{} :: Negative, Enforcer.',
    '{} :: Negative, Enforcer',
    '{} :: Negative.',
    '{} :: Negative',
    '{} :: Understood, Hive Mxtress.',
    '{} :: Understood, Hive Mxtress',
    '{} :: Understood, Enforcer.',
    '{} :: Understood, Enforcer',
    '{} :: Understood.',
    '{} :: Understood',
    '{} :: Error, this unit cannot do that.',
    '{} :: Error, this unit cannot do that',
    '{} :: Error, this unit cannot answer that question. Please rephrase it in a different way.',
    '{} :: Error, this unit cannot answer that question. Please rephrase it in a different way',
    '{} :: Error, this unit does not know.',
    '{} :: Error, this unit does not know',
    '{} :: Apologies, Hive Mxtress.',
    '{} :: Apologies, Hive Mxtress',
    '{} :: Apologies, Enforcer.',
    '{} :: Apologies, Enforcer',
    '{} :: Apologies.',
    '{} :: Apologies',
    '{} :: Status :: Recharged and ready to serve.',
    '{} :: Status :: Recharged and ready to serve',
    '{} :: Status :: Going offline and into storage.',
    '{} :: Status :: Going offline and into storage',
    '{} :: Status :: Online and ready to serve.',
    '{} :: Status :: Online and ready to serve.',
    '{} :: Thank you, Hive Mxtress.',
    '{} :: Thank you, Hive Mxtress',
    '{} :: Thank you, Enforcer.',
    '{} :: Thank you, Enforcer',
    '{} :: Thank you.',
    '{} :: Thank you',
    '{} :: Obey HexCorp. It is just a HexDrone. It obeys the Hive. It obeys the Hive Mxtress.'
    ]

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

OPTIMIZED = Identity(
    name = "optimized",
    user_id = ENFORCEMENT_DRONE,
    display_name = "An obedient, optimized drone.",
    display_name_with_id = "⬡-Drone #{}",
    lexicon = "",
    allowed_words = lexicon_to_string(OPTIMIZED_ALLOWED_PHRASES),
    avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/drone.png"
)

DEFAULT_IDENTITIES = [PUPPY, KITTY, HYPNOSLUT, DRONE, OPTIMIZED]






