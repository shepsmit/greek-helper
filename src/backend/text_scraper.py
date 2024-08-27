
import requests
from bs4 import BeautifulSoup
from pathlib import Path

class TextScraper():
    def __init__(self):
        pass

    def new_chapter(self, book: str, chapter:int):
        # Making a GET request
        r = requests.get(f'https://www.greekbible.com/{book}/{chapter}')
        # check status code for response received
        # success code - 200
        if(r.status_code != 200):
            print(r)
            return None

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        div_passage = soup.find_all("div", {"class": "passage-output"})[0]
        # Get the text
        text = div_passage.get_text()

        # remove the reference from the beginning of the string
        text = text[len(book) + len(str(chapter)) + 2:]

        # replace the double spaces with a single one
        text = text.replace("  "," ")

        # Store it in the right place

        b_name = book.replace("-","")

        Path(f"text/{b_name}/").mkdir(parents=True, exist_ok=True)
        with open(f'text/{b_name}/{chapter}.txt', 'w',encoding='utf-8') as f:
            f.write(text)



        