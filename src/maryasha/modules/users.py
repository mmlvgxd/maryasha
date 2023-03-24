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
from msgspec.json import Decoder
from msgspec.json import Encoder

from typing import Any

from .structs import User
from .structs import Truck
from .structs import Card

from .economy import generate_card_numbers

from ..constants import USERS_PATH


decoder = Decoder(dict[str, User])
encoder = Encoder()


def load() -> dict[str, User]:
    with open(USERS_PATH, 'r') as stream:
        return decoder.decode(stream.read())


def dump(obj__: Any, /) -> None:
    with open(USERS_PATH, 'wb') as stream:
        stream.write(encoder.encode(obj__))


def new(uid: str) -> None:
    users = load()

    if uid not in users:
        numbers = generate_card_numbers()

        users[uid] = User(
            {'1': Truck()},
            {numbers: Card()}
        )

    dump(users)