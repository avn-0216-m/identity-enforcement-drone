from data_classes import Identity, Lexicon

def init_default_identities() -> list:
    print("Initializing default identities.")
    reply = []
    for identity in DEFAULT_IDENTITIES:
        reply.append(f'INSERT INTO identities(name, user_id, display_name, lexicon_id) VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.lexicon_id}");')
    return reply

def init_default_lexicons() -> list:
    print("Initializing default lexicon migration")
    reply = []
    statement = ''
    for lexicons in DEFAULT_LEXICONS:
        statement = 'INSERT INTO lexicons(lexicon_id, word) VALUES'
        for entry in lexicons:
            statement += f'("{entry.lexicon_id}", "{entry.word}")'
            statement += ","
        statement = statement[:-1] #Remove the dangling comma
        statement += ";"
        reply.append(statement)
    return reply

def map_words_list_to_lexicon_list(words: list, id: int) -> list:
    lexicon_list = []
    for word in words:
        lexicon_list.append(Lexicon(lexicon_id = id, word=word))
    return lexicon_list

enforcer_drone = 694984579995533313

PUPPY = Identity(
    name = "puppy",
    user_id = enforcer_drone,
    allowed_words = [],
    lexicon_id = 1,
    avatar = "https://upload.wikimedia.org/wikipedia/commons/2/2b/WelshCorgi.jpeg",
    display_name = "A puppy!",
)

KITTY = Identity(
    name = "kitty",
    user_id = enforcer_drone,
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






