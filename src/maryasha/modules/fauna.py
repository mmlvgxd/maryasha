from dataclasses import dataclass


@dataclass
class Monkey:
    locale: str = 'Обезьяна'
    value: int = 2_500
    rarity: int = 4


@dataclass
class Gorilla:
    locale: str = 'Горилла'
    value: int = 10_000
    rarity: int = 3


@dataclass
class Orangutan:
    locale: str = 'Орангутан'
    value: int = 100_000
    rarity: int = 2