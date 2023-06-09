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
from .....helpers import author, humanize
from .....modules.users import load, new, dump
from .....modules.economy import (
    COLLECT_RANDOM_A_EDGE,
    COLLECT_RANDOM_B_EDGE,
    COLLECT_MONKEY_MULTIPLIER,
    COLLECT_GORILLA_MULTIPLIER,
    COLLECT_ORANGUTAN_MULTIPLIER,
)
from .....constants import EMBED_STD_COLOR, CONTENTS

from crescent import command
from crescent import Group, Plugin, Context
from hikari import Embed


group = Group("economy")
sub_group = group.sub_group("flora")

plugin = Plugin()


NAME = "collect"
DESCRIPTION = "Собрать бананы"


collect_base = "economy/flora/collect/base.txt"
collect_type = "economy/flora/collect/type.txt"
collect_total = "economy/flora/collect/total.txt"


@plugin.include
@group.child
@sub_group.child
@command(name=NAME, description=DESCRIPTION)
class Collect:
    async def main(self) -> None:
        self.embed.description = str()

        MONKEY = self.user.monkey
        GORILLA = self.user.gorilla
        ORANGUTAN = self.user.orangutan

        collected = randint(COLLECT_RANDOM_A_EDGE, COLLECT_RANDOM_B_EDGE)

        monkey_collected = int(COLLECT_MONKEY_MULTIPLIER * MONKEY * collected)
        gorilla_collected = int(COLLECT_GORILLA_MULTIPLIER * GORILLA * collected)
        orangutan_collected = int(COLLECT_ORANGUTAN_MULTIPLIER * ORANGUTAN * collected)

        types = {
            "Обезьяны": [monkey_collected, ":monkey:"],
            "Гориллы": [gorilla_collected, ":gorilla:"],
            "Орангутаны": [orangutan_collected, ":orangutan:"],
        }

        total = collected + monkey_collected + gorilla_collected + orangutan_collected

        with open(CONTENTS + collect_base, "r") as stream:
            content = stream.read()

        self.embed.description = content.format(self.id__, humanize(collected))

        for type__ in types.items():
            name = type__[0]
            properties = type__[1]

            _collected = properties[0]
            emoji = properties[1]

            if _collected != 0:
                with open(CONTENTS + collect_type, "r") as stream:
                    content = stream.read()

                self.embed.description += content.format(emoji, name, _collected)

            else:
                continue

        self.user.banana += total

        dump(self.users)

        with open(CONTENTS + collect_total, "r") as stream:
            content = stream.read()

        self.embed.description += content.format(humanize(total))

    async def callback(self, ctx: Context) -> None:
        self.id__ = str(ctx.user.id)

        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        new(self.id__)
        self.users = load()
        self.user = self.users[self.id__]

        await self.main()
        await ctx.respond(embed=self.embed)
