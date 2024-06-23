from dataclasses import dataclass
from typing import Union
from enum import Enum


class ContextTypeEnum(Enum):
    Vocabulary = 1
    Field = 2


@dataclass
class KeyValuePair:
    key: str
    value: Union[str, int, float, bool]
