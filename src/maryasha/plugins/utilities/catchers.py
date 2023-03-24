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
from crescent import catch_command

from crescent import Plugin
from crescent import Context

from hikari import Embed

from ...modules.errors import NotEnoughBanana
from ...modules.errors import NotEnoughMoney
from ...modules.errors import NotEnoughCash
from ...modules.errors import CardMoneyLimit
from ...modules.errors import TrucksLimit
from ...modules.errors import NegativeAmount

from ...constants import EMBED_ERR_TITLE
from ...constants import EMBED_ERR_COLOR


plugin = Plugin()

embed = Embed(title=EMBED_ERR_TITLE, color=EMBED_ERR_COLOR)


@plugin.include
@catch_command(NotEnoughBanana)
async def not_enough_banana_catcher(exc: NotEnoughBanana, ctx: Context) -> None:
    embed.description = f'`NotEnough`: {exc}'

    await ctx.respond(embed=embed)


@plugin.include
@catch_command(NotEnoughMoney)
async def not_enough_money_catcher(exc: NotEnoughMoney, ctx: Context) -> None:
    embed.description = f'`NotEnoughMoney`: {exc}'

    await ctx.respond(embed=embed)


@plugin.include
@catch_command(NotEnoughCash)
async def not_enough_cash_catcher(exc: NotEnoughCash, ctx: Context) -> None:
    embed.description = f'`NotEnoughCash`: {exc}'

    await ctx.respond(embed=embed)


@plugin.include
@catch_command(CardMoneyLimit)
async def card_money_limit_catcher(exc: CardMoneyLimit, ctx: Context) -> None:
    embed.description = f'`CardMoneyLimit`: {exc}'

    await ctx.respond(embed=embed)


@plugin.include
@catch_command(TrucksLimit)
async def trucks_limit_catcher(exc: TrucksLimit, ctx: Context) -> None:
    embed.description = f'`TrucksLimit`: {exc}'

    await ctx.respond(embed=embed)


@plugin.include
@catch_command(NegativeAmount)
async def negative_amount_catcher(exc: NegativeAmount, ctx: Context) -> None:
    embed.description = f'`NegativeAmount`: {exc}'

    await ctx.respond(embed=embed)