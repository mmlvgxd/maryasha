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
from .types import CardNumbers
from .types import TruckNumber

from msgspec import Struct


# Грузовик
class Truck(Struct):
    """A Maryasha type describing a Truck"""

    # Уровень грузовика
    # Truck level
    level: int = 1
    # Вместимость грузовика
    # Truck capacity
    capacity: int = 0


# Карта
class Card(Struct):
    """A Maryasha type describing a Card"""

    # Уровень карты
    # Card level
    level: int = 1
    # Деньги карты
    # Card money
    money: int = 0


# Пользователь
class User(Struct):
    """A Maryasha type describing a User"""

    trucks: dict[TruckNumber, Truck]  # Грузовики
    cards: dict[CardNumbers, Card]  # Карты

    banana: int = 0  # Бананы

    monkey: int = 0  # Обезьяны
    gorilla: int = 0  # Гориллы
    orangutan: int = 0  # Орангутаны

    cash: int = 0  # Наличные
