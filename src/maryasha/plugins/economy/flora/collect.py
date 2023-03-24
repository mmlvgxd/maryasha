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

from crescent import command

from crescent import Plugin
from crescent import Context

from crescent.ext import locales
from crescent.ext import kebab

from hikari import Embed

from ....helpers.tools import author

from ....modules.users import load
from ....modules.users import dump
from ....modules.users import new

from ....modules.economy import COLLECT_A_END_POINT as CAEP
from ....modules.economy import COLLECT_B_END_POINT as CBEP
from ....modules.economy import COLLECT_MONKEY_MULTIPLIER as CMM
from ....modules.economy import COLLECT_GORILLA_MULTIPLIER as CGM
from ....modules.economy import COLLECT_ORANGUTAN_MULTIPLIER as COM

from ....helpers.emojis import E_B
from ....helpers.emojis import E_M
from ....helpers.emojis import E_G
from ....helpers.emojis import E_O

from ....constants import EMBED_STD_COLOR


plugin = Plugin()

ru_LL = 'Собрать бананы'
en_US_LL = 'Collect bananas'

DESCRIPTION = locales.LocaleMap('floraCollect', ru=ru_LL, en_US=en_US_LL)


@plugin.include
@kebab.ify
@command(description=DESCRIPTION)
class FloraCollect:
    TITLE = 'Сбор'


    async def main(self) -> None:
        self.embed.description = str()

        MONKEY = self.user.monkey
        GORILLA = self.user.gorilla
        ORANGUTAN = self.user.orangutan

        collected = randint(CAEP, CBEP)

        monkey_collected = int(CMM * MONKEY)
        gorilla_collected = int(CGM * GORILLA)
        orangutan_collected = int(COM * ORANGUTAN)

        fauna = {
            'Обезьяны': [monkey_collected, E_M],
            'Гориллы': [gorilla_collected, E_G],
            'Орангутаны': [orangutan_collected, E_O],
        }

        total = \
            collected + \
            monkey_collected + \
            gorilla_collected + \
            orangutan_collected

        self.embed.description = \
            f'<@{self.uid}>, Вы собрали {E_B} `{collected}`шт.'

        for representative in fauna.items():
            name = representative[0]
            properties = representative[1]

            _collected = properties[0]
            emoji = properties[1]

            if _collected != 0:

                self.embed.description += \
                    f'\n+ {emoji} **{name}**: {E_B} `{_collected}`шт.'

            else:
                continue

        self.user.banana += total

        dump(self.users)

        self.embed.description += \
            f'\n\n**Всего**: {E_B} `{total}`шт.'


    async def callback(self, ctx: Context) -> None:
        self.uid = str(ctx.user.id)

        self.embed = Embed(title=self.TITLE, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.uid)
        self.users = load()
        self.user = self.users[self.uid]

        await self.main()

        await ctx.respond(embed=self.embed)