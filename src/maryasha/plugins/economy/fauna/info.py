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
from crescent import command
from crescent import option

from crescent import Group
from crescent import Plugin
from crescent import Context

from crescent.ext import locales
from crescent.ext import kebab

from hikari import Embed

from ....helpers.other import author
from ....helpers.other import sepint

from ....helpers.emojis import E_B
from ....helpers.emojis import E_MW

from ....modules.fauna import Monkey
from ....modules.fauna import Gorilla
from ....modules.fauna import Orangutan

from ....constants import EMBED_STD_COLOR


group = Group("economy")
sub_group = group.sub_group("fauna")

plugin = Plugin()

ru_LL = "Информация о фауне"
en_US_LL = "Information about fauna"

DESCRIPTION = locales.LocaleMap("faunaInfo", ru=ru_LL, en_US=en_US_LL)


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class FaunaInfo:
    TITLE = "Фауна"

    representative = option(
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

        _representative = fauna[self.representative]

        locale = _representative.locale
        value = _representative.value
        rarity = _representative.rarity

        evalue = (
            f":{self.representative}: `/fauna feed {self.representative}`\n"
            f"{E_B} **Стоимость приручения**: `{sepint(value)}`шт.\n"
            f"{E_MW} **Вероятность приручения**: `1/{sepint(rarity)}`"
        )

        self.embed.add_field(name=locale, value=evalue)

    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        await self.main()

        await ctx.respond(embed=self.embed)
