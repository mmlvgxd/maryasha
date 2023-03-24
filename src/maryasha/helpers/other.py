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
from hikari import Embed
from hikari import Member

# Установить автора с именем, равным имени пользователя, и значком, равным аватару
# Set author with name equals username and icon equals avatar
def author(member: Member, embed: Embed) -> None:
    name = member.username
    icon = member.avatar_url

    embed.set_author(name=name, icon=icon)

# Четное ли число
# Is the number even
def is_even(number: int) -> bool:
    if number & 1:
        # Нечетное
        # Odd
        return False
    else:
        # Четное
        # Even
        return True

# Разделить число
# Seperate number
def sepint(number: int) -> str:
    seperator = '_'

    return f'{number:,}'.replace(',', seperator)