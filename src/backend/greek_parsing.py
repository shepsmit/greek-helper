
import requests
from bs4 import BeautifulSoup
from models.utils import InflectedWord

class GreekParser():
    def __init__(self):
        pass

    def newLemma(self, lemma:str):
        print(f"new lemma: {lemma}")
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
                        # print(cols)
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
            print(entry)
            print("\n")

    def getLemmaFromWord(self, word:str):
        # Find word in database

        # Return lemma and parsing
        if(word == "ἀρχῆς"):
            return "ἀρχή"

    def loadLemmaMap(self)->dict:
        with open('lemma_map.csv', mode='r', encoding='utf8') as infile:
            reader = csv.reader(infile)
            d = {}
            for row in reader:
                # Greek Lemma,  ImagePath (missing extension)
                d[row[0]] = row[1] 
        return d