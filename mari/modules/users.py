from msgspec.json import Decoder
from msgspec.json import Encoder

from typing import Any

from .structs import User
from ..constants import USERS_PATH


decoder = Decoder(dict[str, User])
encoder = Encoder()


def load() -> dict[str, User]:
    with open(USERS_PATH, 'r') as stream:
        return decoder.decode(stream.read())


def dump(obj__: Any, /) -> None:
    with open(USERS_PATH, 'w') as stream:
        stream.write(encoder.encode(obj__))
