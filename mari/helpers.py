from hikari import Embed
from hikari import Member


def author(member: Member, embed: Embed) -> None:
    name = member.username
    icon = member.avatar_url

    embed.set_author(name=name, icon=icon)
