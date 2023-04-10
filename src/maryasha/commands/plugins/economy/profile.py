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
from ....helpers import author, humanize
from ....modules.users import load, new
from ....modules.economy import truck_max_capacity, card_max_money
from ....constants import EMBED_STD_COLOR, CONTENTS
from ....modules.errors import DontHaveTrucks

from crescent import command, option
from crescent import Group, Plugin, Context
from hikari import Embed


group = Group("economy")
plugin = Plugin()

NAME = "profile"
DESCRIPTION = "Профиль пользователя"


fauna = "economy/profile/fauna.txt"
flora = "economy/profile/flora.txt"
finance_base = "economy/profile/finance/base.txt"
finance_cards = "economy/profile/finance/cards.txt"
logistic_trucks = "economy/profile/logistic/trucks.txt"


@plugin.include
@group.child
@command(name=NAME, description=DESCRIPTION)
class Profile:
    # fmt: off
    type = option(
        str,
        "Тип",
        choices=[
            ("Фауна", "1"),
            ("Флора", "2"),
            ("Финансы", "3"),
            ("Логистика", "4")
        ],
    )
    # fmt: on

    async def fauna(self) -> None:
        MONKEY = self.user.monkey
        GORILLA = self.user.gorilla
        ORANGUTAN = self.user.orangutan

        with open(CONTENTS + fauna, "r") as stream:
            content = stream.read()

        # fmt: off
        description = content.format(
            humanize(MONKEY),
            humanize(GORILLA),
            humanize(ORANGUTAN)
        )
        # fmt: on

        self.embed.description = description

    async def flora(self) -> None:
        BANANA = self.user.banana

        with open(CONTENTS + flora, "r") as stream:
            content = stream.read()

        description = content.format(humanize(BANANA))

        self.embed.description = description

    async def finance(self) -> None:
        CASH = self.user.cash

        with open(CONTENTS + finance_base, "r") as stream:
            content = stream.read()

        description = content.format(humanize(CASH))

        if self.user.cards is not None:
            for card in self.user.cards.items():
                numbers = card[0]
                properties = card[1]

                level = properties.level
                money = properties.money

                max_money = card_max_money(level)

                with open(CONTENTS + finance_cards, "r") as stream:
                    content = stream.read()

                # fmt: off
                value = content.format(
                    numbers,
                    humanize(level),
                    humanize(money),
                    humanize(max_money)
                )
                # fmt: on

                self.embed.add_field(name="Карты", value=value)

        self.embed.description = description

    async def logistic(self) -> None:
        description = str()

        TRUCKS = self.user.trucks

        if TRUCKS is None:
            for truck in TRUCKS.items():
                index = truck[0]
                properties = truck[1]

                level = properties.level
                capacity = properties.capacity

                max_capacity = truck_max_capacity(level)

                name = f"Грузовик №{index}"

                with open(CONTENTS + logistic_trucks, "r") as stream:
                    content = stream.read()

                # fmt: off
                description += content.format(
                    name,
                    humanize(level),
                    humanize(capacity),
                    humanize(max_capacity)
                )
                # fmt: on
        else:
            raise DontHaveTrucks

        self.embed.description = description

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)
        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        types = {
            "1": self.fauna,
            "2": self.flora,
            "3": self.finance,
            "4": self.logistic,
        }

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        for _type in types.items():
            if self.type == _type[0]:
                await _type[1]()

        await ctx.respond(embed=self.embed)
