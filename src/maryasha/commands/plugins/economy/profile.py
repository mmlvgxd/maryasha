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
from ....modules.structs import User
from ....constants import EMBED_STD_COLOR, CONTENTS_PATH

from crescent import command, option
from crescent import Group, Plugin, Context
from hikari import Embed


group = Group("economy")
plugin = Plugin()

NAME = "profile"
DESCRIPTION = "Профиль пользователя"


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

    async def fauna(self, user: User) -> None:
        MONKEY = user.monkey
        GORILLA = user.gorilla
        ORANGUTAN = user.orangutan

        with open(CONTENTS_PATH + "economy/profile/fauna.txt", "r") as stream:
            content = stream.read()

        # fmt: off
        description = content.format(
            humanize(MONKEY),
            humanize(GORILLA),
            humanize(ORANGUTAN)
        )
        # fmt: on

        self.embed.description = description

    async def flora(self, user: User) -> None:
        BANANA = user.banana

        with open(CONTENTS_PATH + "economy/profile/flora.txt", "r") as stream:
            content = stream.read()

        description = content.format(humanize(BANANA))

        self.embed.description = description

    async def finance(self, user: User) -> None:
        CASH = user.cash

        with open(CONTENTS_PATH + "economy/profile/finance/base.txt", "r") as stream:
            content = stream.read()

        description = content.format(humanize(CASH))

        if user.cards is not None:
            for card in user.cards.items():
                numbers = card[0]
                properties = card[1]

                level = properties.level
                money = properties.money

                max_money = card_max_money(level)

                with open(
                    CONTENTS_PATH + "economy/profile/finance/cards.txt", "r"
                ) as stream:
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

    async def logistic(self, user: User) -> None:
        description = str()

        TRUCKS = user.trucks

        for truck in TRUCKS.items():
            index = truck[0]
            properties = truck[1]

            level = properties.level
            capacity = properties.capacity

            max_capacity = truck_max_capacity(level)

            name = f"Грузовик №{index}"

            with open(
                CONTENTS_PATH + "economy/profile/logistic/trucks.txt", "r"
            ) as stream:
                content = stream.read()

            # fmt: off
            description += content.format(
                name,
                humanize(level),
                humanize(capacity),
                humanize(max_capacity)
            )
            # fmt: on

        self.embed.description = description

    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)
        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        types = {
            "1": self.fauna,
            "2": self.flora,
            "3": self.finance,
            "4": self.logistic,
        }

        new(self.uid)
        users = load()
        user = users[self.uid]

        for _type in types.items():
            if self.type == _type[0]:
                await _type[1](user)

        await ctx.respond(embed=self.embed)
