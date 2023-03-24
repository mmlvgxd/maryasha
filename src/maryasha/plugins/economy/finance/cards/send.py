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
from asyncio import gather

from crescent import command
from crescent import option

from crescent import Plugin
from crescent import Context

from crescent.ext import locales
from crescent.ext import kebab

from hikari import User
from hikari import Embed

from flare import Row
from flare import text_select
from flare import MessageContext

from .....helpers.tools import author

from .....modules.users import load
from .....modules.users import dump
from .....modules.users import new

from .....helpers.emojis import E_C
from .....helpers.emojis import E_CC

from .....constants import W
from .....constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Перевести деньги на карту'
en_US_LL = 'Send money to a card'

DESCRIPTION = locales.LocaleMap('cardsSend', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class CardsSend:
    TITLE = 'Отправить'

    reciever = option(User, 'Получатель')
    amount = option(int, 'Количество денег')


    async def main(self) -> None:
        CARDS = self.user.cards
        RCARDS = self.ruser.cards

        options = list()
        roptions = list()

        for rcard in RCARDS.items():
            roptions.append(rcard[0])


        @text_select(
            placeholder='Карты',
            options=roptions
        )
        async def rmenu(ctx: MessageContext):
            __embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
            author(ctx.member, __embed)

            self.rnumbers = ctx.values[0]

            self.user.cards[self.numbers].money -= self.amount
            self.ruser.cards[self.rnumbers].money += self.amount

            dump(self.users)

            __embed.description = \
                f'{E_CC} <@{self.uid}> отправил <@{self.ruid}>{W}' \
                f'{E_C} `{self.amount}`$'

            await ctx.respond(embed=__embed)


        for card in CARDS.items():
            options.append(card[0])


        @text_select(
            placeholder='Карты',
            options=options
        )
        async def menu(ctx: MessageContext):
            _embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
            author(ctx.member, _embed)

            self.numbers = ctx.values[0]

            _embed.description = f'{E_CC} Выберите карту получателя'
            rcomponents = await gather(Row(rmenu()))

            await ctx.edit_response(embed=_embed, components=rcomponents)


        self.embed.description = f'{E_CC} Выберите Вашу карту'
        components = await gather(Row(menu()))

        return components


    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)
        self.ruid = str(self.reciever.id)

        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        new(self.ruid)
    
        self.users = load()
        self.user = self.users[self.uid]
        self.ruser = self.users[self.ruid]

        components = await self.main()

        await ctx.respond(embed=self.embed, components=components, ephemeral=True)