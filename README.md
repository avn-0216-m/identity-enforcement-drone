# Identity Enforcement Drone #3161

Have you ever wished PluralKit was, like, horny? This is the bot for you.

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