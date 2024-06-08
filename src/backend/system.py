from models.utils import FlashCard, FlashCardContent
import os

class FlashcardSet():
    def __init__(self):
        self.flashcards = []

    def loadFlashcardSet(self):
        files = os.listdir("images")
        for f in files:
            self.flashcards.append(FlashCard(back=f.replace(".png",""), 
                                             back_type=FlashCardContent.TEXT, 
                                             front=f'images/{f}',
                                             front_type=FlashCardContent.IMAGE))