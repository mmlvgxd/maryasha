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

from crescent import Plugin
from crescent import Context

from crescent.ext import kebab
from crescent.ext import locales

from hikari import Embed

from .....helpers import author
from .....helpers import is_even
from .....modules.economy import truck_sell

from .....modules.users import load
from .....modules.users import dump
from .....modules.users import new

from .....emojis import E_T
from .....emojis import E_AL
from .....emojis import E_MWW

from .....constants import W
from .....constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Продать бананы из грузовика'
en_US_LL = 'Sell bananas from the truck'

DESCRIPTION = locales.LocaleMap('logisticTrucksSell', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class TrucksSell:
    TITLE = 'Продажа'


    async def main(self) -> None:
        TRUCKS = self.user.trucks

        TOTAL_EARNINGS = 0
        self.embed.description = str()

        for truck in TRUCKS.items():
            index = truck[0]
            properties = truck[1]

            sold = properties.capacity
            earnings = truck_sell(sold)

            TOTAL_EARNINGS += earnings
            self.user.trucks[index].capacity -= sold

            emoji = E_AL if is_even(int(index)) else E_T

            self.embed.description += \
                f'{emoji} **Грузовик №{index}**{W}' \
                f'продал :banana: `{sold}`шт.{W}' \
                f'за`{earnings}`$\n'

        self.embed.description += \
            f'\n{E_MWW} **Всего продано**:{W}' \
            f'`{TOTAL_EARNINGS}`$'

        self.user.cash += TOTAL_EARNINGS

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
