
import requests
from bs4 import BeautifulSoup
from models.database_models import InflectedWord
from backend.database import DatabaseInterface
from storage.sqllite_config import *
import csv

# Common Words
article_list = ["ὃ","τοῦ","ὅς","τοῖς","τῆς","αἱ" ]
pronoun_list = ["ἡμῶν"]
eimi_list = ["ἦν"]
class GreekParser():
    def __init__(self):
        self.db = DatabaseInterface()

        self.d = self.loadLemmaMap()

    def newLemma(self, lemma:str):
        print(f"new lemma: {lemma}")
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

    def getLemmaFromInflected(self, inflected_word:str)->str:
        # Check for article
        if (inflected_word.lower() in article_list):
            return "ὃ"
        elif (inflected_word.lower() in pronoun_list):
            return "autos"
        elif (inflected_word.lower() in eimi_list):
            return "ειμί"
        # Find word in database
        lemma = self.db.get_lemma_from_inflected(inflected_word)['value']
        return lemma

    def loadLemmaMap(self)->dict:
        with open('src/lemma_map.csv', mode='r', encoding='utf8') as infile:
            reader = csv.reader(infile)
            d = {}
            for row in reader:
                # Greek Lemma,  ImagePath (missing extension)
                d[row[0]] = row[1] 
        return d
    
    def parse_article(word:str):
        i_word = InflectedWord(inflection=word, lemma="ὃ")
        match word:
            case "ὃ": return InflectedWord(inflection=word)
        # article_list = [,"τοῦ","ὅς","τοῖς","τῆς","αἱ" ]
