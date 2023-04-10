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
from typing import Any
from ..constants import USERS

from msgspec import Struct
from msgspec.json import Decoder, Encoder


class Card(Struct):
    level: int = 1
    money: int = 0


class Truck(Struct):
    level: int = 1
    capacity: int = 0


class User(Struct):
    # Flora
    banana: int = 0
    # Fauna
    monkey: int = 0
    gorilla: int = 0
    orangutan: int = 0
    # Finance
    cash: int = 0
    cards: dict[str, Card] | None = None
    # Logistic
    trucks: dict[str, Truck] | None = None


decoder = Decoder(dict[str, User])
encoder = Encoder()


def load() -> dict[str, User]:
    with open(USERS, "r") as stream:
        return decoder.decode(stream.read())


def dump(obj__: Any, /) -> None:
    with open(USERS, "wb") as stream:
        stream.write(encoder.encode(obj__))


def new(id__: str) -> None:
    users = load()

    if id__ not in users:
        users[id__] = User()

    dump(users)
