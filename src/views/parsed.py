
from nicegui import ui
from models.utils import FlashCard
from views.components.navbar import navbar
from views.components.elements import FlashCardContainer
from models.utils import *

class ViewParsed():
    def __init__(self, system):
        self.flashcard_container = None
        self.system = system


        self.update_flag_verse = False
        self.update_flag_chapter = False

        self.setupView()

        
    
    def load_parsed_icons(self, f:FlashCard):
        if(f.case != None):
            match f.case:
                case Case.NOMINATIVE:
                    ui.label("N")
                case Case.GENITIVE:
                    ui.label("G")
                case Case.DATIVE:
                    ui.label("D")
                case Case.ACCUSATIVE:
                    ui.label("A")
                case Case.NOMINATIVE_ACCUSATIVE:
                    ui.label("N|A")
        if(f.tense != None):
            match f.tense:
                case Tense.PRESENT:
                    ui.image("src/images/icons/tense_present.png").classes("w-6 h-10")
                case Tense.IMPERFECT:
                    ui.image("src/images/icons/tense_imperfect.png").classes("w-6 h-6")
                case Tense.FUTURE:
                    ui.image("src/images/icons/tense_future.png").classes("w-6 h-6")
                case Tense.AORIST:
                    ui.image("src/images/icons/tense_aorist.png").classes("w-6 h-10")
                case Tense.FIRST_AORIST:
                    ui.image("src/images/icons/tense_aorist.png").classes("w-6 h-10")
                case Tense.SECOND_AORIST:
                    ui.image("src/images/icons/tense_aorist.png").classes("w-6 h-10")
                case Tense.PERFECT:
                    ui.image("src/images/icons/tense_perfect.png").classes("w-6 h-6")
                case Tense.PLUPERFECT:
                    ui.image("src/images/icons/tense_pluperfect.png").classes("w-6 h-6")
        if(f.voice != None):
            match f.voice:
                case Voice.ACTIVE:
                    ui.image("src/images/icons/voice_active.png").classes("w-7 h-6")
                case Voice.MIDDLE_PASSIVE:
                    ui.image("src/images/icons/voice_middle_passive.png").classes("w-7 h-10")
        if(f.mood != None):
            match f.mood:
                case Mood.INDICATIVE:
                    ui.label(" ")
                case Mood.IMPERATIVE:
                    ui.label("!")
                case Mood.SUBJUNCTIVE:
                    ui.label("?")
                case Mood.OPTATIVE:
                    ui.label("??")
                case Mood.PARTICIPLE:
                    ui.label("P")
                case Mood.INFINITIVE:
                    ui.label("I")
        if(f.person != None):
            match f.person:
                case Person.FIRST:
                    ui.label("1")
                case Person.SECOND:
                    ui.label("2")
                case Person.THIRD:
                    ui.label("3")
        
        if(f.gender != None):
            match f.gender:
                case Gender.FEMININE:
                    ui.image("src/images/icons/gender_feminine.png").classes("w-6 h-6")
                case Gender.MASCULINE:
                    ui.image("src/images/icons/gender_masculine.png").classes("w-6 h-6")
                case Gender.NEUTER:
                    ui.image("src/images/icons/gender_neuter.png").classes("w-6 h-6")
        if(f.number != None):
            match f.number:
                case Number.PLURAL:
                    ui.image("src/images/icons/number_plural.png").classes("w-8 h-6")
                case Number.SINGULAR:
                    ui.image("src/images/icons/number_singular.png").classes("w-6 h-6")

    # Handler for Book Select Element
    def select_book(self, book_index):
        if(self.flashcard_container != None):
            self.system.update_book(book_index)

            self.update_flag_chapter = True # avoid double updates
            self.update_flag_verse = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.book.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num
            self.chapter_select.update()

            self.verse_select.value = self.system.verse_num
            self.verse_select.options = list(range(1,self.system.book.chapter.num_verses()+1))
            self.verse_select.update()

            self.reset_flashcard_view()

    # Handler for Verse Select Element
    def select_verse(self, verse_num):
        if(self.flashcard_container != None):
            if( self.update_flag_verse == False):
                self.system.update_verse(verse_num)
                self.reset_flashcard_view()
            else:
                self.update_flag_verse = False
    
    # Handler for Chapter Select Element
    def select_chapter(self, chapter_num):
        if(self.flashcard_container != None):
            if( self.update_flag_chapter == False):
                self.system.update_chapter(chapter_num)
                self.reset_flashcard_view()
            else:
                self.update_flag_chapter = False
    
    # Handler for Next Verse Button Element
    def next_verse(self):
        if(self.flashcard_container != None):
            self.system.next_verse()

            # Update the Select Elements
            self.update_flag_chapter = True # avoid double updates
            self.update_flag_verse = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num

            self.verse_select.value = self.system.verse_num
            self.verse_select.options = list(range(1,self.system.num_verses+1))


            self.reset_flashcard_view()
    
    # Handler for Previous Verse Button Element
    def previous_verse(self):
        if(self.flashcard_container != None):
            self.system.previous_verse()

            self.update_flag_chapter = True # avoid double updates
            self.update_flag_verse = True # avoid double updates
            self.chapter_select.options = list(range(1,self.system.num_chapters+1))
            self.chapter_select.value = self.system.chapter_num

            self.verse_select.value = self.system.verse_num
            self.verse_select.options = list(range(1,self.system.num_verses+1))

            self.reset_flashcard_view()

    def reset_flashcard_view(self):
        self.flashcard_container.clear()
        with ui.row() as self.flashcard_container:
            for f in self.system.flashcards:
                card_class_str = "items-center"
                with ui.card().classes(card_class_str):
                    FlashCardContainer(flashcard=f, class_str="w-24 h-24 text-center")
                    # Now put the parsing info below the image
                    with ui.row().classes("items-center"):
                        self.load_parsed_icons(f)

    def setupView(self):
        @ui.page('/parsed')
        def page_index():
            with navbar('Parsed', self.system):
                ### Header ###
                with ui.row().classes('w-full items-center'):
                    # Book Name Select
                    self.book_select = ui.select(self.system.book_dict, value=self.system.book_index, on_change=lambda e: self.select_book(e.value)).classes('text-3xl font-bold w-36').props('dense')
                    # Chapter Number Select
                    self.chapter_select = ui.select(list(range(1,self.system.num_chapters+1)), value=self.system.chapter_num, on_change=lambda e: self.select_chapter(e.value)).classes('text-3xl font-bold w-12').props('dense')
                    ui.label(":").classes('text-3xl font-bold')
                    # Verse Number Select
                    self.verse_select = ui.select(list(range(1,self.system.num_verses+1)), value=self.system.verse_num, on_change=lambda e: self.select_verse(e.value)).classes('text-3xl font-bold w-12').props('dense')
                    ui.button(icon="arrow_back_ios", on_click=lambda: self.previous_verse()).props('dense')
                    ui.button(icon="arrow_forward_ios", on_click=lambda: self.next_verse()).props('dense')


                    with ui.row() as fc:
                        self.flashcard_container = fc
                        self.reset_flashcard_view()

                
                            
