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
from ......helpers import author, humanize
from ......modules.users import load, dump, new
from ......modules.economy import card_max_money
from ......constants import EMBED_STD_COLOR, CONTENTS_PATH
from ......modules.errors import NegativeAmount, CardMoneyLimit, NotEnoughMoney

from crescent import command, option
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed
from flare import Row, MessageContext, text_select


group = Group("economy")
sub_group = group.sub_group("finance")

plugin = Plugin()


DESCRIPTION = "Снять деньги с карты"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class CardsWithdraw:
    TITLE = "Снять"

    amount = option(int, "Количество денег")

    async def main(self) -> None:
        CARDS = self.user.cards

        options = []

        for card in CARDS.items():
            options.append(card[0])

        @text_select(placeholder="Карты", options=options)
        async def menu(ctx: MessageContext):
            numbers = ctx.values[0]

            CARD = CARDS[numbers]
            LEVEL = CARD.level

            if self.amount < 0:
                raise NegativeAmount

            elif self.amount > card_max_money(LEVEL):
                raise CardMoneyLimit

            if self.amount <= CARD.money:
                _embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
                author(ctx.member, _embed)

                self.user.cash += self.amount
                self.user.cards[numbers].money -= self.amount

                dump(self.users)

                with open(
                    CONTENTS_PATH + "economy/finance/cards/up.txt", "r"
                ) as stream:
                    content = stream.read()

                _embed.description = content.format(humanize(self.amount))

                await ctx.respond(embed=_embed)
            else:
                raise NotEnoughMoney

        self.embed.description = ":credit_card: Выберите Вашу карту"
        components = await gather(Row(menu()))

        return components

    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        self.users = load()
        self.user = self.users[self.uid]

        components = await self.main()

        await ctx.respond(embed=self.embed, components=components, ephemeral=True)
