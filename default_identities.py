from data_classes import Identity
from notable_entities import ENFORCEMENT_DRONE
from serialize import lexicon_to_string

TEMPLATE = Identity(
        name = None,
        description = None,
        display_name = None,
        display_name_with_id = None,
        avatar = None,
        replacement_lexicon = "",
        allowance_lexicon = "",
        strict = 0,
        override_lexicon = "",
        override_chance = 0,
        user_id = None
        )

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

PUPPY = Identity(
        name = "Puppy",
        description = "Wuff wuff! This is a default identity created by the identity enforcement drone!",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/puppy.jpeg",
        replacement_lexicon = lexicon_to_string(PUPPY_WORDS),
        allowance_lexicon = None,
        strict = 0,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE
    )

KITTEN_WORDS = [
    "meow", 
    "meow!",
    "mrow", 
    "prrrr",
    "maiou!!!",
    ":3",
    "meww~",
    "meow~!",
    "prr! prrrr~",
    "prr prrrrr...",
    "🐾🐈"
    ]

KITTEN = Identity(
        name = "Kitten",
        description = "Meoww~! This is a default identity created by the identity enforcement drone!",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/kitty.jpg",
        replacement_lexicon = lexicon_to_string(KITTEN_WORDS),
        allowance_lexicon = None,
        strict = 0,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE
    )

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

HYPNOSLUT = Identity(
        name = "Hypnoslut",
        description = "Sink deeper and deeper with this zonked-out default identity. <3",
        display_name = None,
        display_name_with_id = None,
        avatar = "https://raw.githubusercontent.com/avn-0216-m/identity-enforcement-images/master/puppy.jpeg",
        replacement_lexicon = lexicon_to_string(HYPNOSLUT_WORDS),
        allowance_lexicon = None,
        strict = 0,
        override_lexicon = None,
        override_chance = 0,
        user_id = ENFORCEMENT_DRONE
    )

DEFAULT_IDENTITIES = [PUPPY, KITTEN, HYPNOSLUT]






