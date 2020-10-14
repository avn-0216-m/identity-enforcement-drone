# Identities

![](identities.png)

(That's puppyspeak for "This is me with an identity").

Identities are created by users and enforced by the bot. For details on how to create an identity, check [the commands list](./COMMANDS.md).

Identities have many fields which are used for informational and enforcement purposes, which will be explained now:

## Name (name)
This is the name of the identity itself. It is used for reference purposes only. This is the identifier you will use when enforcing someone (e.g `!id enforce @maiden Drone`, where "Drone" is the name).

## Description (description)
Similar to name, this field is purely informational.

## Display Name (written as display_name)
This is the display name users enforced with your identity will have. If a user has the `display_name` of `Good toy`, then all the messages sent by them will appear to be sent by `Good toy`.

## Avatar (avatar)
If this attribute is set to a valid URL, it will replace the user's current avatar when enforcing an identity.

## Replacement Lexicon (replacement_lexicon)
This lexicon makes up the words that a user's message is replaced with. For example, a replacement lexicon with "beep" and "boop" in it would replace a user message with a random pattern of "beep" and "boop" until it is roughly the same length as the original message.

## Allowance Lexicon (allowance_lexicon)

## Strict (strict)

## Disallowance Lexicon (disallowance_lexicon)

## Override Lexicon (override_lexicon)

## Override Chance (override_chance)

## How the Lexicons Interact

An identity will behave differently depending on the lexicons present. Here is an overview:

### Replacement
With just a replacement lexicon, a new message will be built using words and phrases from the replacement lexicon until it is roughly the same length as the original message.

### Allowance
With just an allowance lexicon, the message will be deleted unless it is an exact match of one of the entires in the allowance lexicon.

### Replacement, Allowance
With an allowance lexicon and replacement lexicon present in an identity, the message will still be replaced by the replacement lexicon, but any allowed words and phrases from the original message will be spliced into the replacement message. For example, a puppy identity with "yes miss!" in the allowance lexicon would turn "yes miss! i love being a puppy!!" into "yes miss! woof woof bark snff"

### Disallowance
With just a disallowance lexicon, any disallowed words or phrases will be replaced with underscores. For example, "think" would become "\_\_\_\_\_". The number of characters is preserved when disallowing words.

### Disallowance, Replacement
With a disallowance lexicon and a replacement lexicon, disallowed words will be replaced with words from the replacement lexicon until roughly equivalent length.

### Disallowance, Allowance
No effect. The identity will default to behaving as if it only has an allowance lexicon.

### Replacement, Allowance, Disallowance
No effect. The identity will default to behaving as if it only has a disallowance and replacement lexicon.

### Override
No matter what combination of lexicons an identity has, there will always be a chance for the override to automatically replace the message provided the chance is greater than 0.