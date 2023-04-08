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
from ......modules.economy import truck_max_capacity
from ......modules.users import load, dump, new
from ......constants import EMBED_STD_COLOR, CONTENTS_PATH

from crescent import command
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("logistic")

plugin = Plugin()


DESCRIPTION = "Поместить бананы в грузовики"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class TrucksPut:
    TITLE = "Вмещение"

    async def main(self) -> None:
        BANANA = self.user.banana
        TRUCKS = self.user.trucks

        self.embed.description = str()

        for truck in TRUCKS.items():
            number = truck[0]
            properties = truck[1]

            level = properties.level
            capacity = properties.capacity

            max_capacity = truck_max_capacity(level)

            emoji = ":articulated_lorry:" if is_even(int(number)) else ":truck:"

            if capacity >= max_capacity:
                with open(
                    CONTENTS_PATH + "economy/logistic/trucks/put/full.txt", "r"
                ) as stream:
                    content = stream.read()

                self.embed.description += content.format(
                    emoji, number, humanize(capacity), humanize(max_capacity)
                )

                continue

            total = capacity
            _total = 0

            while BANANA > 0:
                if total == max_capacity:
                    break

                total += 1
                _total += 1
                BANANA -= 1

            with open(
                CONTENTS_PATH + "economy/logistic/trucks/put/base.txt", "r"
            ) as stream:
                content = stream.read()

            self.embed.description += content.format(
                humanize(total), humanize(max_capacity), emoji, number
            )

            self.user.trucks[number].capacity += _total

        with open(CONTENTS_PATH + "economy/logistic/trucks/put/end.txt", "r") as stream:
            content = stream.read()

        self.embed.description += content.format(humanize(BANANA))

        self.user.banana = BANANA

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
