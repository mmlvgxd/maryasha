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
from .....helpers import author, humanize
from .....modules.fauna import Monkey, Gorilla, Orangutan
from .....constants import EMBED_STD_COLOR, CONTENTS

from crescent import command, option
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("fauna")

plugin = Plugin()


DESCRIPTION = "Информация о фауне"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class FaunaInformation:
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

        _locale__ = type__.locale
        _value__ = type__.value
        _rarity__ = type__.rarity

        with open(CONTENTS, "r") as stream:
            content = stream.read()

        _value = content.format(self.type, humanize(_value__), humanize(_rarity__))

        self.embed.add_field(name=_locale__, value=_value)

    async def callback(self, ctx: Context) -> None:
        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        await self.main()
        await ctx.respond(embed=self.embed)
