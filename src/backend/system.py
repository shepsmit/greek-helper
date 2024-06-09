from models.utils import *
from backend.greek_parsing import GreekParser
import csv
import os
import re

class FlashCardSet():
    def __init__(self, chapter_name):
        self.greek_parser = GreekParser()
        self.flashcards = []
        self.chapter = self.loadGreekChapter(chapter_name)
        # self.greek_parser.newLemma("ἀρχή")

    def getFlashCardSetChapterWords(self)-> list:
        set = []
        for verse_item in self.chapter.verses.items():
            verse_num = verse_item[0]
            set += self.getFlashCardSetVerseWords(verse_num)
        return set
                
    def getFlashCardSetVerseWords(self, verse_num: int)->list:
        set = []
        verse = self.chapter.verses[verse_num]
        for word in verse.words:

            lemma = self.greek_parser.getLemmaFromWord(word)

            set.append(FlashCard(front=word, 
                                front_type=FlashCardContent.TEXT, 
                                back=f'images/{lemma}.png',
                                back_type=FlashCardContent.IMAGE))
        return set
            

    def loadFlashCardSetImages(self):
        files = os.listdir("images")
        for f in files:
            self.flashcards.append(FlashCard(back=f.replace(".png",""), 
                                             back_type=FlashCardContent.TEXT, 
                                             front=f'images/{f}',
                                             front_type=FlashCardContent.IMAGE))
            
    def loadGreekChapter(self, chapter_name:str)->Chapter:
        file_path = f"text/{chapter_name.lower().replace(" ","")}.txt"
        with open(file_path, encoding='utf8') as f:
            txt = f.read()
        
        c = Chapter(reference=chapter_name)
        
        verses_text  = re.findall(r"\d+(\D+)", txt) # split by verse number
        for i, v_text in enumerate(verses_text):
            
            v_new = Verse(text=v_text)
            v_text = v_text.replace(",","").replace(".","").strip()
            v_words = v_text.split(" ")
            v_new.words = v_words
            c.verses[i+1] = v_new

        return(c)
    
