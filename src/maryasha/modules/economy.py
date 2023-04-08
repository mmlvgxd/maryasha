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

# Точки грани случайного числа заработка
COLLECT_RANDOM_A_EDGE = 120
COLLECT_RANDOM_B_EDGE = 340
# Множитель заработка представителей фауны
COLLECT_MONKEY_MULTIPLIER = 1.3
COLLECT_GORILLA_MULTIPLIER = 2.2
COLLECT_ORANGUTAN_MULTIPLIER = 3.1
# Максимальная вместимость грузовика
# Зависимая от уровня
def truck_max_capacity(level: int) -> int:
    multiplier = 2_500  # Множитель вместимости

    return int(level * multiplier)
# Стоимость следующего грузовика
# Зависимая от текущего количества грузовиков
def truck_cost(amount: int) -> int:
    multiplier = 5_000  # Множитель стоимости

    return int(amount * multiplier)
# Стоимость следующего уровня грузовика
# Зависимое от текущего уровня
def truck_level_cost(level: int) -> int:
    multiplier = 1_250  # Множитель стоимости

    return int(level * multiplier)
# Продажа бананов из грузовиков
# Зависимая от количества бананов
def truck_sell(amount: int) -> int:
    multiplier = 0.5  # Множитель продажи

    return int(amount * multiplier)

# Генерация номера карты
def card_numbers_generator() -> str:
    numbers = []

    for _ in range(4):
        numbers.append(str(randint(1_000, 9_999)))

    return "-".join(numbers)
# Максималное количество денег карты
# Зависимое от уровня
def card_max_money(level: int) -> int:
    multiplier = 10_000  # Множитель денег

    return int(level * multiplier)
# Стоимость следующего уровня карты
# Зависимая от текущего уровня
def card_level_cost(level: int) -> int:
    multiplier = 2_500  # Множитель стоимости

    return int(level * multiplier)
