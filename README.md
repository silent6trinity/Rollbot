# Rollbot
A stupid-simple Discord attendance bot in python.

Set the bot up within your developer portal, and provide the proper permissions needed to access messages and voice channel members.

The attendance is taken based off the `Discord Roles` assigned to server members. The bot only works when invoked from the corresponding meeting chat.

*Example*:
(In the Voice chat's text channel):
`/rollcall <role>` - Provides a list of all the members of a given `Role` that _are not_ within the voice chat currently.


`/list <role>` - Provides a list of all members within a provided `Role`
