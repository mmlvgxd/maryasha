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

from ..constants import W

# Точки грани случайного числа заработка
COLLECT_A_END_POINT = 120
COLLECT_B_END_POINT = 340
# Множитель заработка представителей фауны
COLLECT_MONKEY_MULTIPLIER = 1.3
COLLECT_GORILLA_MULTIPLIER = 2.2
COLLECT_ORANGUTAN_MULTIPLIER = 3.1

# Максимальная вместимость грузовика
# Зависимая от уровня
def truck_max_capacity(level: int) -> int:
    multiplier = 2500 # Множитель вместимости

    return int(level * multiplier)

# Стоимость следующего грузовика
# Зависимая от текущего количества грузовиков
def truck_cost(amount: int) -> int:
    multiplier = 5000 # Множитель стоимости

    return int(amount * multiplier)

# Стоимость следующего уровня грузовика
# Зависимое от текущего уровня
def truck_level_cost(level: int) -> int:
    multiplier = 1250 # Множитель стоимости

    return int(level * multiplier)

# Продажа бананов из грузовиков
# Зависимая от количества бананов
def truck_sell(amount: int) -> int:
    multiplier = 0.5

    return int(amount * multiplier)

# Генерация номера карты
def generate_card_numbers() -> str:
    numbers = []

    for _ in range(4):
        numbers.append(str(randint(1000, 9999)))

    return f'{W}'.join(numbers)
