from models.utils import *
import os
import re

class FlashCardSet():
    def __init__(self):
        self.flashcards = []
        self.chapter = self.loadGreekChapter("1 John 1")

    def loadFlashCardSetWords(self):
        for verse_item in self.chapter.verses.items():
            verse_num = verse_item[0]
            verse = verse_item[1]
            for word in verse.words:
                self.flashcards.append(FlashCard(back=verse_num, 
                                                back_type=FlashCardContent.TEXT, 
                                                front=word,
                                                front_type=FlashCardContent.TEXT))
            

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