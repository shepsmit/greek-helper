
import requests
from bs4 import BeautifulSoup
from models.database_models import InflectedWord
from backend.database import DatabaseInterface
from storage.sqllite_config import *
import csv
from models.utils import *

# https://myluthernet.luthersem.edu/ICS/icsfs/PrincipalPartsAlpha.pdf?target=a5b23532-b3ac-4ce9-b8e7-92d110d5414b
principal_parts = {
    "λέγω" : "λέγω, ἐρῶ, εἶπον, εἴρηκα, εἴρημαι, ἐρρέθην",
    "ἔχω" : "ἔχω, ἕξω, ἔσχον, ἔσχηκα, -, -",
    "γίνομαι":"γίνομαι, γενήσομαι, ἐγενόμην, γέγονα, γεγένημαι, ἐγενήθην",
    "ἔρχομαι":"ἔρχομαι, ἐλεύσομαι, ἦλθον , ἐλήλυθα, -, -",
    "δίδωμι" : "δίδωμι, δώσω, ἔδωκα, δέδωκα, δέδομαι, ἐδόθην",
    "λαμβάνω" : "λαμβάνω, λήμψομαι, ἔλαβον, εἴληφα, εἴλημμαι, ἐλήμφθην",
    "γράφω" : "γράφω, γράψω, ἔγραψα, γέγραφα, γέγραμμαι, ἐγράφην",
    "γινώσκω" : "γινώσκω, γνώσομαι, ἔγνων, ἔγνωκα, ἔγνωσμαι, ἐγνώσθην",
    "ὁράω" : "ὁράω, ὄψομαι, ὠψάμην, ἑώρακα, ὤμμαι, ὤφθην",
}

# Common Words
article_list = ["ὁ","τοῦ","τοῖς","τῆς","αἱ" ]

pronoun_1_2_list = ["ἐγώ","ἡμᾶς","ἡμεῖς","ἡμῶν", "ἡμῖν", "ὑμῖν","ὑμεῖς","μου"]
pronoun_3_list = ["αὐτός","αὐτός", "αὐτοῦ","αὐτῷ",]
relative_pronoun_list = ["ὃ","ὅς","ὅστις","ἐκεῖνος","οὗτος"]
conjunctions = ["καί","ἵνα","οὐ","ὡς","καί","μή","οὐδέ","καθώς","ὅτι"]
common = ["εἰ"]
prepositions = ["μετά","ἀπό","ἐν","πρός","περί","ἀλλά","ὅτι","ἄν","διά","εἰς"]
names = ["Ἰησοῦς"]
eimi_list = ["ειμί","ἦν","ἔστιν","ἐστιν","ἐστίν","ἔστιν·","ἐστὶν","ἐσμεν·","εἶναι","ἐστε"]

SKIP_WORDS = common + article_list + eimi_list + pronoun_1_2_list + pronoun_3_list + relative_pronoun_list + prepositions + names + conjunctions

class GreekParser():
    def __init__(self):
        self.db = DatabaseInterface()

        # self.d = self.load_lemma_map()

        # new_word = True
        new_word = False
        if(new_word):
            entry = InflectedWord(inflection="ἕν", lemma="ἐν", parsing="indecl", translation="in")
            self.new_lemma_manual(entry)

    def get_cached_lemmas(self, book:str, chapter_num:int)->list:
        return self.db.get_lemmas(book,chapter_num)


    def new_lemma_manual(self, entry: InflectedWord):
        self.db.insert_inflected(entry)

    def new_lemma(self, lemma:str):
        # print(f"new lemma: {lemma}")
        # check to see if this lemma is already in the database
        if(self.db.already_has_lemma(lemma)['value'] == True):
            print("Lemma already in Database")
            return None

        else:
            # Making a GET request
            r = requests.get(f'https://lexicon.katabiblon.com/index.php?lemma={lemma}')
            # check status code for response received
            # success code - 200
            if(r.status_code != 200):
                print(r)
                return None

            inflected_entries = []
            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')
            table_list = soup.find_all('table')
            # element_list = soup.find_all('tr')
            for table in table_list:
                if("Lemma" in table.get_text()):
                    # Get the table rows
                    entry_list = table.find_all("tr")
                    for e in entry_list:
                        new_e  = InflectedWord()
                        # Get the table entries
                        cols = e.find_all("td")
                        if(len(cols)>=7):
                            # Fill out the new entry with the table columns
                            new_e.inflection        = cols[1].get_text()
                            new_e.lemma             = cols[2].get_text()
                            new_e.uncontracted_form = cols[3].get_text()
                            new_e.parsing           = cols[4].get_text()
                            new_e.translation       = cols[5].get_text()
                            new_e.verse             = cols[6].get_text()

                            inflected_entries.append(new_e)
                    break # just the first one please (NT only)
            for entry in inflected_entries:
                self.db.insert_inflected(entry)

    def get_parsed_inflected(self, book_name, chapter_num, inflected_word:str)->InflectedWord:
        # Check for article
        if (inflected_word.lower() in article_list):
            return self.parse_article(inflected_word.lower())
        elif (inflected_word.lower() in eimi_list):
            return self.parse_eimi(inflected_word.lower())
        # Find word in database
        word = self.db.parse_inflected(book_name.replace(" ",""), chapter_num, inflected_word)['value']
        # print(f'{word.inflection} {word.lemma}')
        return word

    def load_lemma_map(self)->dict:
        with open('src/lemma_map.csv', mode='r', encoding='utf8') as infile:
            reader = csv.reader(infile)
            d = {}
            for row in reader:
                # Greek Lemma,  ImagePath (missing extension)
                d[row[0]] = row[1] 
        return d
    
    def parse_article(self, word:str)->InflectedWord:
        i_word = InflectedWord(inflection=word, lemma="ὁ")

        match word:
            case "ὁ":
                i_word.gender = Gender.MASCULINE
                i_word.case   = Case.NOMINATIVE
                i_word.number = Number.SINGULAR
            case "τοῦ":
                i_word.gender = Gender.MASCULINE
                i_word.case   = Case.GENITIVE
                i_word.number = Number.SINGULAR
            case "τοῖς":
                i_word.gender = Gender.MASCULINE
                i_word.case   = Case.DATIVE
                i_word.number = Number.PLURAL
            case "τῆς":
                i_word.gender = Gender.FEMININE
                i_word.case   = Case.GENITIVE
                i_word.number = Number.SINGULAR
            case "αἱ":
                i_word.gender = Gender.FEMININE
                i_word.case   = Case.NOMINATIVE
                i_word.number = Number.PLURAL
        return i_word

    def parse_eimi(self, word:str)->InflectedWord:
        i_word = InflectedWord(inflection=word, lemma="ειμί")
        match word:
            case "ἦν":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.IMPERFECT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE

            case "ἔστιν":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἐστιν":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἐστίν":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἔστιν·":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἐστὶν":
                i_word.person = Person.THIRD
                i_word.number = Number.SINGULAR
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἐσμεν·":
                i_word.person = Person.FIRST
                i_word.number = Number.PLURAL
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "ἐστε":
                i_word.person = Person.SECOND
                i_word.number = Number.PLURAL
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INDICATIVE
                i_word.voice  = Voice.ACTIVE
            case "εἶναι":
                i_word.tense  = Tense.PRESENT
                i_word.mood   = Mood.INFINITIVE
                i_word.voice  = Voice.ACTIVE

                
        return i_word
    
   

        i_word = InflectedWord(inflection=word, lemma="ὅς")
        match word:
            case "ὅς":
                i_word.gender = Gender.MASCULINE
                i_word.case   = Case.NOMINATIVE
                i_word.number = Number.SINGULAR
            case "ὃ":
                i_word.gender = Gender.NEUTER
                i_word.case   = Case.NOMINATIVE
                i_word.number = Number.SINGULAR
        return i_word