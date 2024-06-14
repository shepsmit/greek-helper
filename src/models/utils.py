from dataclasses import dataclass, field
from collections import defaultdict
from typing import List
from enum import Enum

class Number(Enum):
    SINGULAR = 0, # Icon: One Person
    PLURAL = 1    # Icon: Crowd

class Mood(Enum):
    INDICATIVE = 0,  # Default
    IMPERATIVE = 1,  # Exclamation Point
    SUBJUNCTIVE = 2, # Question?
    OPTATIVE = 3,    # ?
    PARTICIPLE = 4,  # ?
    INFINITIVE = 5   # ?

class Voice(Enum):
    ACTIVE = 0,         # ?
    MIDDLE_PASSIVE = 1, # ?

class Person(Enum):
    FIRST  = 0,  # Icon: Point at Me
    SECOND = 1,  # Icon: Point at You
    THIRD  = 2   # Icon: Point at Them

class Gender(Enum):
    MASCULINE = 0, # Border Color
    FEMININE  = 1, # Border Color
    NEUTER = 2,    # Border Color
    MASCULINE_FEMININE = 3, # ?
    MASCULINE_NEUTER = 4,   # ?

class Case(Enum):
    NOMINATIVE = 0, # ?
    GENITIVE = 1,   # ?
    DATIVE = 2,     # ?
    ACCUSATIVE = 3, # ?
    NOMINATIVE_ACCUSATIVE = 4 # ?

class Tense(Enum):
    PRESENT = 0,
    IMPERFECT = 1,
    AORIST = 2,
    FUTURE = 3,
    PERFECT = 4,
    PLUPERFECT = 5,
    FIRST_AORIST = 6,
    SECOND_AORIST = 7,




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
    gender: Gender = None
    case: Case = None
    number: Number = None
    tense: Tense = None
    mood: Mood = None
    voice: Voice = None
    person: Person = None



