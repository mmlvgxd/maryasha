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
from ....helpers import author
from ....constants import EMBED_STD_COLOR, CONTENTS_PATH

from crescent import command
from crescent import Group, Plugin, Context
from hikari import Embed


group = Group("utilities")

plugin = Plugin()


NAME = "ping"
DESCRIPTION = "Просмотр статуса бота"


@plugin.include
@group.child
@command(name=NAME, description=DESCRIPTION)
class Ping:
    async def callback(self, ctx: Context) -> None:
        with open(CONTENTS_PATH + "utilities/ping.txt", "r") as stream:
            content = stream.read()

        self.uid = str(ctx.user.id)
        self.embed = Embed(title=DESCRIPTION, color=EMBED_STD_COLOR)
        author(ctx.member, self.embed)

        self.embed.description = content

        await ctx.respond(embed=self.embed)
