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

from .....helpers.tools import author
from .....modules.economy import truck_cost

from .....modules.users import load
from .....modules.users import new

from .....helpers.emojis import E_MWW

from .....constants import W
from .....constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Информация о грузовиках'
en_US_LL = 'Information about trucks'

DESCRIPTION = locales.LocaleMap('logisticTrucksInfo', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class TrucksInfo:
    TITLE = 'Информация'


    async def main(self) -> None:
        TRUCKS = self.user.trucks
        amount = len(TRUCKS.items()) + 1

        if not amount > 10:
            cost = truck_cost(amount)

            self.embed.description = \
                f'{E_MWW} **Цена грузовика**:{W}' \
                f'`{cost}`$'


    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        self.users = load()
        self.user = self.users[self.uid]

        await self.main()

        await ctx.respond(embed=self.embed)