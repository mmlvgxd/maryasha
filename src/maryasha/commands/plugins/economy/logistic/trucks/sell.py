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
from ......helpers import author, humanize, is_even
from ......modules.economy import truck_sell
from ......modules.users import load, dump, new
from ......constants import EMBED_STD_COLOR, CONTENTS_PATH

from crescent import command
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("logistic")

plugin = Plugin()


DESCRIPTION = "Продать бананы из грузовика"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class TrucksSell:
    TITLE = "Продажа"

    async def main(self) -> None:
        TRUCKS = self.user.trucks

        TOTAL_EARNINGS = 0
        self.embed.description = str()

        for truck in TRUCKS.items():
            number = truck[0]
            properties = truck[1]

            sold = properties.capacity
            earnings = truck_sell(sold)

            TOTAL_EARNINGS += earnings
            self.user.trucks[number].capacity -= sold

            emoji = ":articulated_lorry:" if is_even(int(number)) else ":truck:"

            with open(
                CONTENTS_PATH + "economy/logistic/trucks/sell/base.txt", "r"
            ) as stream:
                content = stream.read()

            self.embed.description += content.format(
                emoji, number, humanize(sold), humanize(earnings)
            )

        with open(
            CONTENTS_PATH + "economy/logistic/trucks/sell/total.txt", "r"
        ) as stream:
            content = stream.read()

        self.embed.description += content.format(humanize(TOTAL_EARNINGS))

        self.user.cash += TOTAL_EARNINGS

        dump(self.users)

    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        self.users = load()
        self.user = self.users[self.uid]

        await self.main()

        await ctx.respond(embed=self.embed)
