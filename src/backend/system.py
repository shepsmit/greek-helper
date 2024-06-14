from models.utils import *
from backend.greek_parsing import GreekParser
import csv
import os
import re

class FlashCardSet():
    def __init__(self, chapter_name):
        self.greek_parser = GreekParser()
        self.flashcards = []
        self.chapter = self.load_greek_chapter(chapter_name)
        # self.chapter.printChapter()


    def get_flashcard_set_chapter_words(self)-> list:
        set = []
        for verse_item in self.chapter.verses.items():
            verse_num = verse_item[0]
            set += self.get_flashcard_set_verse_words(verse_num)
        return set
                
    def get_flashcard_set_verse_words(self, verse_num: int)->list:
        set = []
        verse = self.chapter.verses[verse_num]
        for word in verse.words:
            parsed_word = self.greek_parser.get_parsed_inflected(word)
            fc = FlashCard()
            
            if os.path.exists(f'src/images/{parsed_word.lemma}.png'):
                fc.front=f'src/images/{parsed_word.lemma}.png' 
                fc.front_type=FlashCardContent.IMAGE

            else:
                fc.front=parsed_word.lemma 
                fc.front_type=FlashCardContent.TEXT 

            fc.back=word
            fc.back_type=FlashCardContent.TEXT

            fc.gender = parsed_word.gender
            fc.case = parsed_word.case
            fc.number = parsed_word.number
            fc.tense = parsed_word.tense
            fc.mood = parsed_word.mood
            fc.voice = parsed_word.voice
            fc.person = parsed_word.person
            
            set.append(fc)
            

        return set
            

    def load_flashcard_set_images(self):
        files = os.listdir("src/images")
        for f in files:
            self.flashcards.append(FlashCard(back=f.replace(".png",""), 
                                             back_type=FlashCardContent.TEXT, 
                                             front=f'src.images/{f}',
                                             front_type=FlashCardContent.IMAGE))
            
    def load_greek_chapter(self, chapter_name:str)->Chapter:
        file_path = f"src/text/{chapter_name.lower().replace(" ","")}.txt"
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
    
