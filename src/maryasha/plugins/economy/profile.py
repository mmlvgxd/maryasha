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
from crescent import option

from crescent import Plugin
from crescent import Context

from hikari import Embed

from crescent.ext import kebab
from crescent.ext import locales

from ...helpers.tools import author

from ...modules.users import load
from ...modules.users import new

from ...modules.economy import truck_max_capacity
from ...modules.economy import card_max_money

from ...modules.structs import User

from ...helpers.emojis import E_C
from ...helpers.emojis import E_T
from ...helpers.emojis import E_B
from ...helpers.emojis import E_M
from ...helpers.emojis import E_G
from ...helpers.emojis import E_O
from ...helpers.emojis import E_CC
from ...helpers.emojis import E_PC
from ...helpers.emojis import E_MWW

from ...constants import W
from ...constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Профиль пользователя'
en_US_LL = 'Profile of the user'

DESCRIPTION = locales.LocaleMap('profile', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class Profile:
    TITLE = 'Профиль'

    type = option(str, 'Тип опции', choices=[
        ('Фауна', '1'),
        ('Флора', '2'),
        ('Финансы', '3'),
        ('Логистика', '4')
    ])


    async def fauna(self, user: User) -> None:
        MONKEY = user.monkey
        GORILLA = user.gorilla
        ORANGUTAN = user.orangutan

        description = \
            f'{E_M} **Обезьян**: `{MONKEY}`шт.\n' \
            f'{E_G} **Горилл**: `{GORILLA}`шт.\n' \
            f'{E_O} **Орангутанов**: `{ORANGUTAN}`шт.'

        self.embed.description = description


    async def flora(self, user: User) -> None:
        BANANA = user.banana

        description = f'{E_B} **Бананов**: `{BANANA}`шт.'

        self.embed.description = description


    async def finance(self, user: User) -> None:
        CASH = user.cash

        description = f'{E_MWW} **Наличных**: `{CASH}`$'

        if user.cards is not None:

            for card in user.cards.items():
                numbers = card[0]
                properties = card[1]

                level = properties.level
                money = properties.money

                max_money = card_max_money(level)

                value = \
                    f'{E_CC} ||{numbers}||\n' \
                    f'> {E_PC} **Уровень**: `{level}`ур.\n' \
                    f'> {E_C} **Денег**: `{money}`/`{max_money}`$'

                self.embed.add_field(name='Карты', value=value)

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

            name = f'Грузовик №{index}'

            description += \
                f'{E_T} **{name}**\n' \
                f'> {E_PC} **Уровень**: `{level}`ур.\n' \
                f'> {E_B} **Вместимость**:{W}' \
                f'`{capacity}`/`{max_capacity}`шт.\n'

        self.embed.description = description


    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)
        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        types = {
            '1': self.fauna,
            '2': self.flora,
            '3': self.finance,
            '4': self.logistic
        }

        new(self.uid)
        users = load()
        user = users[self.uid]

        for _type in types.items():
            if self.type == _type[0]:
                await _type[1](user)

        await ctx.respond(embed=self.embed)
