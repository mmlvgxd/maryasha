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
from hikari import Color
from hikari import Status
from hikari import Activity

from . import __version__

# Пробел
# Whitespace
W = ' '
# Статус & Активность бота
# Status & Activity of the bot
STATUS = Status.IDLE
ACTIVITY = Activity(name=f'v{__version__}')
# Путь до пользователей
# Path to users
USERS_PATH = './users.json'
# Названия для эмбеда
# Title for embed
EMBED_ERR_TITLE = 'Ошибка!'
# Цвета для эмбедов
# Colors for embeds
EMBED_STD_COLOR = Color.from_rgb(159, 157, 207)
EMBED_ERR_COLOR = Color.from_rgb(255, 75, 75)
