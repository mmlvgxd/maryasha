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
from ......modules.economy import truck_cost
from ......modules.users import load, new
from ......modules.errors import TrucksLimit
from ......constants import EMBED_STD_COLOR, CONTENTS

from crescent import command
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("logistic")

plugin = Plugin()


DESCRIPTION = "Информация о грузовиках"


trucks_information = "economy/logistic/trucks/information.txt"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class TrucksInformation:
    async def main(self) -> None:
        TRUCKS = self.user.trucks
        amount = len(TRUCKS.items()) + 1

        if amount <= 10:
            cost = truck_cost(amount)

            with open(CONTENTS + trucks_information, "r") as stream:
                content = stream.read()

            self.embed.description = content.format(humanize(cost))
        else:
            raise TrucksLimit

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        await self.main()
        await ctx.respond(embed=self.embed)
