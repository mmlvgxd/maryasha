from msgspec import Struct


class Config(Struct):
    '''A Mari type describing a Config'''
    token: str


class Truck(Struct):
    '''A Mari type describing a Truck'''
    level: int
    capacity: int


class Card(Struct):
    '''A Mari type describing a Card'''
    level: int
    money: int


class User(Struct):
    '''A Mari type describing a User'''
    banana: int

    monkey: int
    gorilla: int
    orangutan: int

    cash: int

    trucks: dict[str, Truck]
    cards: dict[str, Card]