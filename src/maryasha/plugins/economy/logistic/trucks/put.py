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

from crescent import Group
from crescent import Plugin
from crescent import Context

from crescent.ext import kebab
from crescent.ext import locales

from hikari import Embed

from .....helpers.other import author
from .....helpers.other import sepint
from .....helpers.other import is_even
from .....modules.economy import truck_max_capacity

from .....modules.users import load
from .....modules.users import dump
from .....modules.users import new

from .....helpers.emojis import E_T
from .....helpers.emojis import E_B
from .....helpers.emojis import E_AL

from .....constants import W
from .....constants import EMBED_STD_COLOR


group = Group("economy")
sub_group = group.sub_group("logistic")

plugin = Plugin()

ru_LL = "Поместить бананы в грузовики"
en_US_LL = "Put bananas in trucks"

DESCRIPTION = locales.LocaleMap("logisticTrucksPut", ru=ru_LL, en_US=en_US_LL)


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

            emoji = E_AL if is_even(int(number)) else E_T

            if capacity >= max_capacity:
                self.embed.description += (
                    f"{emoji} **Грузовик №{number}**{W}"
                    f"полность заполнен{W}"
                    f"(`{sepint(capacity)}`/`{sepint(max_capacity)}`)\n"
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

            self.embed.description += (
                f"Вместили `{sepint(total)}`/`{sepint(max_capacity)}`{W}"
                f"в {emoji} **Грузовик №{number}**\n"
            )

            self.user.trucks[number].capacity += _total

        self.embed.description += (
            f"\nОсталось вместить {E_B}{W}" f"`{sepint(BANANA)}`шт."
        )

        self.user.banana = BANANA

        dump(self.users)

    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        self.users = load()
        self.user = self.users[self.uid]

        await self.main()

        await ctx.respond(embed=self.embed)
