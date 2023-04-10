# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2023 mmlvgx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from random import randint
from .....helpers import author
from .....modules.users import load, dump, new
from .....modules.errors import NotEnoughBanana
from .....modules.fauna import Monkey, Gorilla, Orangutan
from .....constants import EMBED_STD_COLOR, CONTENTS

from crescent import command, option
from crescent.ext import kebab
from crescent import Group, Plugin, Context
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("fauna")

plugin = Plugin()


DESCRIPTION = "Покормить и приручить представителя фауны"


feed_succes = "economy/fauna/feed/succes.txt"
feed_failure = "economy/fauna/feed/failure.txt"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class FaunaFeed:
    type = option(
        str,
        "Тип",
        choices=[
            (Monkey.locale, "monkey"),
            (Gorilla.locale, "gorilla"),
            (Orangutan.locale, "orangutan"),
        ],
    )

    async def main(self) -> None:
        fauna = {"monkey": Monkey, "gorilla": Gorilla, "orangutan": Orangutan}

        type__ = fauna[self.type]

        _type__locale = type__.locale
        _type__value = type__.value
        _type__rarity = type__.rarity

        if self.user.banana > _type__value:
            self.user.banana -= _type__value

            if randint(1, _type__rarity) == 1:
                self.embed.title = "Успешно!"

                with open(CONTENTS + feed_succes, "r") as stream:
                    content = stream.read()

                self.embed.description = content.format(self.type, _type__locale)

                if type__ is Monkey:
                    self.user.monkey += 1
                elif type__ is Gorilla:
                    self.user.gorilla += 1
                elif type__ is Orangutan:
                    self.user.orangutan += 1

                dump(self.users)

                return

            self.embed.title = "Упс!"

            with open(CONTENTS + feed_failure, "r") as stream:
                content = stream.read()

            self.embed.description = content.format(self.type, _type__locale)
        else:
            raise NotEnoughBanana

        

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        await self.main()
        await ctx.respond(embed=self.embed)
