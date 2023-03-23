from msgspec.json import Decoder

from .structs import Config
from ..constants import CONFIG_PATH


decoder = Decoder(type=Config)

with open(CONFIG_PATH, 'r') as stream:
    config = decoder.decode(stream.read())
