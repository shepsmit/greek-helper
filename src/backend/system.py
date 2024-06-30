from models.utils import *
from backend.greek_parsing import GreekParser
import csv
import os
import re

class FlashCardSet():
    def __init__(self):
        self.greek_parser = GreekParser()
        self.flashcards = []
        # self.chapter.printChapter()

        self.book_dict = {1:"1 John",
                          2:"2 John"}
        self.book_index = 1
        self.chapter_num = 2
        self.chapter = self.load_greek_chapter(self.book_dict[self.book_index], self.chapter_num)

        self.verse_num = 1
        self.num_chapters = 5
        self.num_verses = self.chapter.num_verses()
        self.flashcards = None

        self.load_flashcard_set()


    def load_flashcard_set(self):
        self.flashcards = self.get_flashcard_set_verse_words(self.verse_num)


    def update_book(self, book_index:int):
        if(book_index > 0 and book_index <= len(self.book_dict.keys())):
            self.book_index = book_index
            self.update_chapter(number=1)            


    def update_verse(self, number:int):
        if(number > 0 and number <= self.chapter.num_verses()):
            self.verse_num = number
            self.load_flashcard_set()


    def update_chapter(self, number:int):
        if(number > 0 and number <= self.num_chapters):
            self.chapter_num = int(number)
            self.chapter = self.load_greek_chapter(self.book_dict[self.book_index], self.chapter_num)
            self.verse_num = 1
            self.num_verses = self.chapter.num_verses()
            self.load_flashcard_set()

    def next_verse(self):
        # Go to the next verse
        if(self.verse_num < self.num_verses):
            self.update_verse(self.verse_num + 1)
        else:
            # Go to the next chapter
            if(self.chapter_num < self.num_chapters):
                self.update_chapter(self.chapter_num + 1)
        
    def previous_verse(self):
        # Go back one verse
        if(self.verse_num > 1):
            self.update_verse(self.verse_num - 1)
        # Go to the last verse of the previous chapter
        else:
            if(self.chapter_num > 1):
                self.update_chapter(self.chapter_num - 1)
                self.update_verse(self.num_verses)

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
                # print(f'\tsrc/images/{parsed_word.lemma}.png')

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
            
    def load_greek_chapter(self, book_name:str, chapter_num:int)->Chapter:
        file_path = f"src/text/{book_name.lower().replace(" ","")}/{str(chapter_num)}.txt"
        with open(file_path, encoding='utf8') as f:
            txt = f.read()
        
        c = Chapter(book_name, chapter_num)
        
        verses_text  = re.findall(r"\d+(\D+)", txt) # split by verse number
        for i, v_text in enumerate(verses_text):
            
            v_new = Verse(text=v_text)
            v_text = v_text.replace(",","").replace(".","").strip()
            v_words = v_text.split(" ")
            v_new.words = v_words
            c.verses[i+1] = v_new

        return(c)
    
