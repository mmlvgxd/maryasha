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
from ......helpers import author, humanize
from ......modules.economy import truck_level_cost
from ......modules.users import load, new, dump
from ......constants import EMBED_STD_COLOR, CONTENTS
from ......modules.errors import NotEnoughCash

from crescent import command, option
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("logistic")

plugin = Plugin()


DESCRIPTION = "Повысить уровень грузовика"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class TrucksUp:
    number = option(str, "Номер грузовика", default=None)

    async def main(self) -> None:
        CASH = self.user.cash
        TRUCKS = self.user.trucks

        TRUCK = TRUCKS[self.number]
        LEVEL = TRUCK.level

        NEXT_LEVEL = LEVEL + 1
        cost = truck_level_cost(NEXT_LEVEL)

        if CASH > cost:
            name = f"Грузовик №{self.number}"

            with open(CONTENTS + "economy/logistic/trucks/up.txt", "r") as stream:
                content = stream.read()

            self.embed.description = content.format(
                self.id__, name, NEXT_LEVEL, humanize(cost)
            )

            self.user.trucks[self.number].level = NEXT_LEVEL
            self.user.cash -= cost

            dump(self.users)
        else:
            raise NotEnoughCash

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        await self.main()
        await ctx.respond(embed=self.embed)
