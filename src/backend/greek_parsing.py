
import requests
from bs4 import BeautifulSoup

class GreekParser():
    def __init__(self):
        pass

    def newLemma(self, lemma:str):
        print(f"new lemma: {lemma}")
        # Making a GET request
        r = requests.get(f'https://lexicon.katabiblon.com/index.php?lemma={lemma}')

        # check status code for response received
        # success code - 200
        print(r)

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        # s = soup.find_all('form', class_='entry-content')
        element_list = soup.find_all('table')
        for element in element_list:
            if("Lemma" in element.get_text()):
                print(element)
        # content = s.find_all('table')
        # print(s)
        # content = s.find_all('p')


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