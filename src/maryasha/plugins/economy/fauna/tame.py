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
from asyncio import gather

from crescent import command
from crescent import option

from crescent import Plugin
from crescent import Context

from crescent.ext import locales
from crescent.ext import kebab

from flare import Row
from flare import button
from flare import MessageContext

from hikari import Embed
from hikari import ButtonStyle

from ....helpers.other import author

from ....modules.users import load
from ....modules.users import dump
from ....modules.users import new

from ....modules.fauna import Monkey
from ....modules.fauna import Gorilla
from ....modules.fauna import Orangutan

from ....helpers.emojis import E_X
from ....helpers.emojis import E_MW
from ....helpers.emojis import E_WCM

from ....constants import W
from ....constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Приручить представителя фауны'
en_US_LL = 'Tame a representative of the fauna'

DESCRIPTION = locales.LocaleMap('faunaTame', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class FaunaTame:
    TITLE = 'Приручение'


    representative = option(str, 'Тип', choices=[
        (Monkey.locale, 'monkey'),
        (Gorilla.locale, 'gorilla'),
        (Orangutan.locale, 'orangutan')
    ])


    async def main(self) -> None:
        fauna = {
            'monkey': Monkey,
            'gorilla': Gorilla,
            'orangutan': Orangutan
        }

        _representative = fauna[self.representative]

        locale = _representative.locale
        value = _representative.value
        rarity = _representative.rarity


        if self.user.banana > value:
            self.user.banana -= value

            if randint(1, rarity) == 1:
                self.embed.title = 'Успешно!'
                self.embed.description = \
                    f'{E_MW} {E_WCM} Вы смогли приручить{W}' \
                    f':{self.representative}: **{locale}**!'

                if _representative is Monkey:
                    self.user.monkey += 1
                elif _representative is Gorilla:
                    self.user.gorilla += 1
                elif _representative is Orangutan:
                    self.user.orangutan += 1

                dump(self.users)

                return

            self.embed.title = 'Упс!'
            self.embed.description = \
                f'{E_MW} {E_X} Вам не удалось приручить{W}' \
                f':{self.representative}: **{locale}**!'
        else:
            return

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