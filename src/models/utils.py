from dataclasses import dataclass
from enum import Enum

class FlashCardContent(Enum):
    TEXT = 0
    IMAGE = 1

class FlashCardSide(Enum):
    FRONT = 0
    BACK = 1


@dataclass
class FlashCard:
    front: str = ""
    front_type:FlashCardContent = None
    back: str = ""
    back_type:FlashCardContent = None



