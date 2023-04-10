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
from ......modules.users import load, new, dump
from ......modules.economy import card_level_cost
from ......constants import EMBED_STD_COLOR, CONTENTS
from ......modules.errors import NotEnoughMoney

from crescent import command
from crescent import Group, Plugin, Context
from crescent.ext import kebab
from hikari import Embed
from flare import Row, MessageContext, text_select


group = Group("economy")
sub_group = group.sub_group("finance")

plugin = Plugin()


DESCRIPTION = "Повысить уровень карты"


cards_up = "economy/finance/cards/up.txt"


@plugin.include
@group.child
@sub_group.child
@kebab.ify
@command(description=DESCRIPTION)
class CardsUp:
    TITLE = "Повысить уровень"

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
            NEXT_LEVEL = LEVEL + 1

            cost = card_level_cost(NEXT_LEVEL)

            if cost <= CARD.money:
                self.user.cards[numbers].level += 1
                self.user.cards[numbers].money -= cost

                dump(self.users)

                with open(CONTENTS + cards_up, "r") as stream:
                    content = stream.read()

                self.embed.description = content.format(
                    humanize(NEXT_LEVEL), humanize(cost)
                )

                await ctx.respond(embed=self.embed)
            else:
                raise NotEnoughMoney

        self.embed.description = ":credit_card: Выберите Вашу карту"
        components = await gather(Row(menu()))

        return components

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        components = await self.main(self.id__)
        await ctx.respond(embed=self.embed, components=components, ephemeral=True)
