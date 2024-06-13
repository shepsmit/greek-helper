from dataclasses import dataclass, field
from collections import defaultdict
from typing import List
from enum import Enum

class Gender(Enum):
    MASC = 0,
    FEM  = 1,
    NEUT = 2

class Case(Enum):
    NOM = 0,
    GEN = 1,
    DAT = 2,
    ACC = 3

class Number(Enum):
    SING = 0,
    PLUR = 1

class FlashCardContent(Enum):
    TEXT = 0
    IMAGE = 1

class FlashCardSide(Enum):
    FRONT = 0
    BACK = 1

@dataclass
class Chapter:
    reference: str = ""
    verses: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))

    def printChapter(self)->None:
        print(self.reference)
        for k in self.verses.keys():
            print(f'{k}: {self.verses[k].text}')



@dataclass
class Verse:
    text: str = ""
    words: List = field(default_factory=lambda: [])

@dataclass
class FlashCard:
    front: str = ""
    front_type:FlashCardContent = None
    back: str = ""
    back_type:FlashCardContent = None



