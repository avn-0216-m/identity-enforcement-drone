from data_classes import Identity
from notable_entities import ENFORCEMENT_DRONE
from serialize import lexicon_to_string

def init_default_identities_for_guild(guild_id) -> list:
    print("Initializing default identities.")

    print("HELLO WORLD")
    print(lexicon_to_string(PUPPY_WORDS))

    reply = []
    for id in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, display_name, display_name_with_id, avatar, replacement_lexicon, allowance_lexicon, strict, override_lexicon, override_chance, owner_type, owner_id, colour) '
        + f'VALUES("{id.name}", "{id.display_name}", "{id.display_name_with_id}", "{id.avatar}", "{id.replacement_lexicon}", "{id.allowance_lexicon}", {id.strict}, "{id.override_lexicon}", {id.override_chance}, "guild", "{guild_id}", "{id.colour}");')

        print("Let's double check")
        for command in reply:
            print(command)
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

TEMPLATE = Identity(
        name = None,
        display_name = None,
        display_name_with_id = None,
        avatar = None,
        replacement_lexicon = "",
        allowance_lexicon = "",
        strict = 0,
        override_lexicon = "",
        override_chance = 0,
        user_id = None,
        colour = None
)

PUPPY = Identity(
        name = "Puppy",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/puppy.jpeg",
        replacement_lexicon = lexicon_to_string(PUPPY_WORDS),
        allowance_lexicon = None,
        strict = 0,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE,
        colour = "FF66FF"
)

STRICT_PUPPY = Identity(
        name = "Strict_Puppy",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/puppy.jpeg",
        replacement_lexicon = None,
        allowance_lexicon = lexicon_to_string(["Hello", "World"]),
        strict = 1,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE,
        colour = "FF66FF"
)

EZ_PUPPY = Identity(
        name = "EZ_Puppy",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/puppy.jpeg",
        replacement_lexicon = None,
        allowance_lexicon = lexicon_to_string(["Hello", "World"]),
        strict = 0,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE,
        colour = "FF66FF"
)

DEFAULT_IDENTITIES = [PUPPY, STRICT_PUPPY, EZ_PUPPY]






