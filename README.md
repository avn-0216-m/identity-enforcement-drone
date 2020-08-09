# Identity Enforcement Drone #3161

Have you ever wished PluralKit was, like, horny? This is the bot for you.

# Identites

Identities are the foundation of this bot. They come with a few attributes:

- name: The name of the identity. Case sensitive. Used for identification so users can find identities easier.
- description: The description of the identity. Similarly used for identification.
- avatar: The picture that will be used when enforcing an identity.
- display_name: The display name that will replace an enforced users original display name when enforcing an identity.
- replacement_lexicon: A list of words and phrases that will be used to build a "replacement message" roughly the length of the user's original message.
- user_id: The discord ID of the identity's owner. Not usually used.

# Commands

Any parameter in [square brackets] is mandatory, anything in \<these weird bois\> is optional.

## Relationships.

`!rl`, also usable as `!rel`, `!relationship`, and `!relationships` is the command group centered around domming and subbing. You must be domming a user (and they must have submitted back to you) to enforce them with an identity.

### !rl

Aliases: `rel`, `relationship`, `relationships`

Usage: `!rl`

By itself, this command will list all confirmed relationships within the server the command was invoked with.

### !rl sub

Aliases: `submit`

Usage: `!rl sub @user`

This command submits (heh) a submission request to the user you mention. If the user responds by dominating you, a successful relationship is confirmed and you two can now engage in fun horny identity play.

### !rl dom

Aliases: `dominate`

Usage: `!rl dom @user`

This command submits a domination request to the user you mention. It's the same as above but, y'know, opposite.

### !rl relinquish

Aliases: `yeet`, `uncollar`

Usage: `!rl relinquish @user`

This command will end any relationship you have with the mentioned user, either as a submissive or a dominant.

### !rl pending

Aliases: None

Usage: `!rl pending`

This command lists all _incoming_ pending requests on the current server (e.g who wants to dom you, who wants to sub for you). This command does not list outbound pending requests (who _you_ want to sub/dom for).

### !rl pending clear

Aliases: None

Usage: `!rl pending clear`

Deletes all incoming pending requests. Clear your head and have a fresh start. Uwah~!

## Identities.

The fun part!

`!id`, also usable as `!ids`, `!identity`, and `!identities`, is the command group for, you guessed it, managing and enforcing identities.

### !id

Aliases: `!ids`, `!identity`, `!identities`

Usage: `!id <@user(s)>`

By itself, the command lists all of your identities, from first to most recently created, with their name and description. If you tag one or more users, it will list their identities instead.

### !id enforce 

Aliases: None

Usage: `!id enforce [@user] [identity name]`

This command creates a new enforcement with the specified identity and target, provided you have that identity in your inventory, and that you are domming the target.

### !id release

Aliases: None

Usage: `!id release [@user]`

This command releases a user from their enforcement, assuming they are already enforced. Currently, anyone can release anyone from enforcement, including themselves.

### !id new

Aliases: None

Usage: `!id new [name] \<description> <replacement_lexicon words>`

Example: `!id new Ara "A very good puppy!" woof bark "please pet me!" bark bark!! bork!!`

This command creates a new identity, provided you do not already have an identity with the same name. You can initialize the identity with just a name, or give it a description and replacement lexicon words for easy setup. If you want a lexicon word to be made of multiple words, please enclose that phrase in quotes, as seen in the example above.

### !id delete

Aliases: None

Usage: `!id delete [name] please`

Example: `!id delete Ara please`

This command deletes an identity in your inventory. You have to add "please" at the end of the request so you don't accidentally delete a command. That'd be no fun at all.

### !id view

Aliases: None

Usage: `!id view [name] [attribute]`

Example: `!id view Puppy avatar`

This commmand lets you view attributes attached to an identity. Simple as.

### !id set

Aliases: None

Usage: `!id set [name] [attribute] [value(s)]`

Example: `!id set Puppy replacement_lexicon meow "meoew please pet me!" meow mew!! hiss~!!`

This command lets you set attributes for an identity. Simple as. Same as when you created an identity like in the `!id new`, enclose anything you want as a single sentence with spaces in quotation marks (e.g `"hello world"` not `hello world`).

## Other commands

### !puppet

Aliases: `!assume-direct-control`, `!puppeteer`, `!amplify`

Usage: `!puppet [@user] [message]`

Example: `!puppet @Aracelle "I should be locked in chastity forever!"`

This command makes a user, who is submissive to you, speak for you.

### !init

Aliases: `!defaults`, `!gimmie`

Usage: `!init`

Example: `!init` (Shocker, I know)

This command will give you the three basic identites that come built in with this bot: Puppy, Kitten, and Hypnoslut (one of these things is not like the other).

**WARNING**: This will overwrite any identities with the same name. Please refrain from using this command if you have a "Puppy"/"Kitten"/"Hypnoslut" identity you'd like to keep.