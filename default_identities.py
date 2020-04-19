from data_classes import Identity

enforcer_drone = 694984579995533313

PUPPY = Identity(
    name = "puppy",
    user_id = enforcer_drone,
    allowed_words = [],
    avatar = "https://upload.wikimedia.org/wikipedia/commons/2/2b/WelshCorgi.jpeg",
    uses_drone_id = False,
    display_name = "A puppy!",
)

KITTY = Identity(
    name = "kitty",
    user_id = enforcer_drone,
    allowed_words = [],
    avatar = "",
    display_name = "A kitty!",
)



ALL = [PUPPY]

def initialize_default_identities() -> list:
    reply = []
    for identity in ALL:
        print(identity)
        reply.append(f'INSERT INTO identities(name, user_id, display_name, avatar_url) VALUES("{identity.name}", "{identity.user_id}", "{identity.display_name}", "{identity.avatar_url}");')
    return reply


