
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

    def parseQuery(self, query: list):
        """Parse a SQLLite query response into individual parameters"""
        self.id                 = int(query[0])
        self.inflection         = str(query[1].decode("utf-8"))
        if("," in self.inflection):
            self.inflection = self.inflection.split(",")[0]
        self.lemma              = str(query[2].decode("utf-8"))
        if ("or" in self.lemma):
            self.lemma = self.lemma.split(" ")[0]
        self.uncontracted_form  = str(query[3].decode("utf-8"))
        self.parsing            = str(query[4])
        self.translation        = str(query[5])
        self.verse              = str(query[6])



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
