
from dataclasses import dataclass
from models.utils import *

## Database Inflected Table
@dataclass
class InflectedWord:
    """
    SQLLite Database Version Table Interface
    """
    id: int = None
    inflection: str	= ""
    lemma: str = ""
    uncontracted_form: str	= ""
    parsing: str = ""	
    translation: str = ""
    verse: str = ""
    gender: Gender = None
    case: Case = None
    number: Number = None
    tense: Tense = None
    mood: Mood = None
    voice: Voice = None
    person: Person = None

    def parseQuery(self, query: list):
        """Parse a SQLLite query response into individual parameters"""
        self.id                 = int(query[0])
        self.inflection         = str(query[1].decode("utf-8"))
        if("," in self.inflection):
            self.inflection = self.inflection.split(",")[0]
        self.lemma              = str(query[2].decode("utf-8"))
        if ("or" in self.lemma):
            self.lemma = self.lemma.split(" ")[0]
        if ("," in self.lemma):
            self.lemma = self.lemma.split(",")[0]
        self.uncontracted_form  = str(query[3].decode("utf-8"))
        self.parsing            = str(query[4])
        if (" or " in self.parsing):
            self.parsing = self.parsing.split(" or ")[0]
        self.unpack_parsing()

        self.translation        = str(query[5])
        self.verse              = str(query[6])


    def unpack_parsing(self)->None:
        # Gender
        if ("mas" in self.parsing and "fem" in self.parsing):
            self.gender = Gender.MASCULINE_FEMININE
        elif "mas" in self.parsing:
            self.gender = Gender.MASCULINE
        elif "fem" in self.parsing:
            self.gender = Gender.FEMININE
        elif "neu" in self.parsing:
            self.gender = Gender.NEUTER
        # Case
        if ("nom" in self.parsing and "acc" in self.parsing):
            self.case = Case.NOMINATIVE_ACCUSATIVE
        elif "acc" in self.parsing:
            self.case = Case.ACCUSATIVE
        elif "nom" in self.parsing:
            self.case = Case.NOMINATIVE
        elif "dat" in self.parsing:
            self.case = Case.DATIVE
        elif "gen" in self.parsing:
            self.case = Case.GENITIVE
        # Number
        if "sg" in self.parsing:
            self.number = Number.SINGULAR
        elif "pl" in self.parsing:
            self.number = Number.PLURAL
        # Tense
        if "1aor" in self.parsing:
            self.tense = Tense.FIRST_AORIST
        elif "2aor" in self.parsing:
            self.tense = Tense.SECOND_AORIST
        elif "pres" in self.parsing:
            self.tense = Tense.PRESENT
        elif "fut" in self.parsing:
            self.tense = Tense.FUTURE
        elif "impf" in self.parsing:
            self.tense = Tense.IMPERFECT
        elif "aor" in self.parsing:
            self.tense = Tense.AORIST
        elif "perf" in self.parsing:
            self.tense = Tense.PERFECT
        elif "plup" in self.parsing:
            self.tense = Tense.PLUPERFECT
        # Mood
        if "ind" in self.parsing:
            self.mood = Mood.INDICATIVE
        elif "sub" in self.parsing:
            self.mood = Mood.SUBJUNCTIVE
        elif "ptcp" in self.parsing:
            self.mood = Mood.PARTICIPLE
        elif "inf" in self.parsing:
            self.mood = Mood.INFINITIVE
        elif "opt" in self.parsing:
            self.mood = Mood.OPTATIVE
        elif "imp" in self.parsing:
            self.mood = Mood.IMPERATIVE    
        # Voice
        if "act" in self.parsing:
            self.voice = Voice.ACTIVE
        elif "mp" in self.parsing:
            self.voice = Voice.MIDDLE_PASSIVE
        # Person
        if "1st" in self.parsing:
            self.person = Person.FIRST
        elif "2nd" in self.parsing:
            self.person = Person.SECOND
        elif "3rd" in self.parsing:
            self.person = Person.THIRD
        
        

    def getInsertParams(self) -> list:
        """Return the SQLLite parameter list"""
        return [self.id,        
                self.inflection.encode("utf-8"),
                self.lemma.encode("utf-8"),
                self.uncontracted_form.encode("utf-8"),
                self.parsing,
                self.translation,
                self.verse            
        ]
