
from nicegui import ui
from models.utils import FlashCard
from views.components.navbar import navbar
from views.components.elements import FlashCardContainer
from models.utils import *

class ViewVocab():
    def __init__(self, system):
        self.flashcard_container = None
        self.system = system

        

        self.update_flag_chapter = False

        self.setupView()

    # Handler for Book Select Element
    def select_book(self, book_index):
        if(self.flashcard_container != None):
            self.system.update_book(book_index)

            self.update_flag_chapter = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.book.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num
            self.chapter_select.update()

            self.reset_flashcard_view()

    # Handler for Chapter Select Element
    def select_chapter(self, chapter_num):
        if(self.flashcard_container != None):
            if( self.update_flag_chapter == False):
                self.system.update_chapter(chapter_num)
                self.reset_flashcard_view()
            else:
                self.update_flag_chapter = False
    
    # Handler for Next Chapter Button Element
    def next_chapter(self):
        if(self.flashcard_container != None):
            self.system.next_chapter()

            # Update the Select Elements
            self.update_flag_chapter = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num

            self.reset_flashcard_view()
    
    # Handler for Previous Verse Button Element
    def previous_chapter(self):
        if(self.flashcard_container != None):
            self.system.previous_chapter()

            self.update_flag_chapter = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num

            self.reset_flashcard_view()

    def reset_flashcard_view(self):
        self.flashcard_container.clear()
        with ui.row() as self.flashcard_container:
            for f in self.system.flashcards:
                card_class_str = "items-center"
                with ui.card().classes(card_class_str):
                    FlashCardContainer(flashcard=f, class_str="w-24 h-24 text-center")
                    

    def setupView(self):
        @ui.page('/vocab')
        def page_index():
            with navbar("Vocab", self.system):
                ### Header ###
                with ui.row().classes('w-full items-center'):
                    # Book Name Select
                    self.book_select = ui.select(self.system.book_dict, value=self.system.book_index, on_change=lambda e: self.select_book(e.value)).classes('text-3xl font-bold w-36').props('dense')
                    # Chapter Number Select
                    self.chapter_select = ui.select(list(range(1,self.system.num_chapters+1)), value=self.system.chapter_num, on_change=lambda e: self.select_chapter(e.value)).classes('text-3xl font-bold w-12').props('dense')
                    ui.button(icon="arrow_back_ios", on_click=lambda: self.previous_chapter()).props('dense')
                    ui.button(icon="arrow_forward_ios", on_click=lambda: self.next_chapter()).props('dense')

                    with ui.row() as fc:
                        self.flashcard_container = fc
                        self.reset_flashcard_view()

                
                            
