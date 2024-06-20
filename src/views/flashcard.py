
from nicegui import ui
from backend.system import FlashCardSet
from models.utils import FlashCard, FlashCardSide, FlashCardContent
from views.components.navbar import navbar
from models.utils import *

def getFlashCardElement(flashcard: FlashCard, side:FlashCardSide, class_str):

    if(side == FlashCardSide.FRONT):
        if(flashcard.front_type == FlashCardContent.IMAGE):
            return (ui.image(flashcard.front).classes(class_str))
        elif(flashcard.front_type == FlashCardContent.TEXT):
            return (ui.label(flashcard.front).classes(class_str))
    
    if(side == FlashCardSide.BACK):
        if(flashcard.back_type == FlashCardContent.IMAGE):
            return (ui.image(flashcard.back).classes(class_str))
        elif(flashcard.back_type == FlashCardContent.TEXT):
            return (ui.label(flashcard.back).classes(class_str))



class FlashCardContainer(ui.card):
    def __init__(self, flashcard: FlashCard, class_str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._side = FlashCardSide.FRONT
        self.flashcard = flashcard
        self.on('click', self.toggle)

        self.class_str = class_str

        with self: # default for front
            getFlashCardElement(self.flashcard, self._side, self.class_str)


    def toggle(self) -> None:
        """Toggle the container state."""
        if(self._side == FlashCardSide.FRONT):
            self._side = FlashCardSide.BACK
        else:
            self._side = FlashCardSide.FRONT
        self.clear()
        with self:
            c = getFlashCardElement(self.flashcard, self._side, self.class_str)
            c.update()

        self.update()

    def update(self) -> None:
        # Code here during updates
        super().update()

class ViewFlashCard():
    def __init__(self):
        self.setupView()

        self.chapter_name = "1 John"
        self.chapter_num = 1
        self.verse_num = 1
        self.num_chapters = 5
        self.num_verses = 10
        
    
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


    def reset_flashcard_view(self, chapter_num:int, verse_num:int):

        if(chapter_num <= self.num_chapters):
            temp_fset = FlashCardSet(f'{self.chapter_name} {int(self.chapter_num)}')
            if(verse_num <= self.fset.chapter.num_verses()):
                self.verse_num = verse_num
                self.chapter_num = chapter_num
                self.fset = temp_fset
                self.num_verses = self.fset.chapter.num_verses()
                self.flashcard_container.clear()

                with ui.row() as self.flashcard_container:
                    self.load_flashcard_view(verse_num)

    def load_flashcard_view(self, verse_num:int):
        f_cards = self.fset.get_flashcard_set_verse_words(verse_num)
        for f in f_cards:
            card_class_str = "items-center"
            with ui.card().classes(card_class_str):
                FlashCardContainer(flashcard=f, class_str="w-24 h-24 text-center")
                # Now put the parsing info below the image
                with ui.row().classes("items-center"):
                    self.load_parsed_icons(f)

    def setupView(self):
        @ui.page('/')
        def page_index():
            with navbar('Session In Progress'):
                ### Header ###
                with ui.row().classes('w-full items-center'):
                    ui.label(self.chapter_name).classes('text-3xl font-bold')
                    self.fset = FlashCardSet(f'{self.chapter_name} {int(self.chapter_num)}')

                    ui.number( value=1, min=1,
                        on_change=lambda e: self.reset_flashcard_view(chapter_num=e.value, verse_num=1)).classes('text-3xl font-bold w-12').props('dense')

                    ui.number( value=1, min=1,
                        on_change=lambda e: self.reset_flashcard_view(chapter_num=self.chapter_num, verse_num=e.value)).classes('text-3xl font-bold w-12').props('dense').bind_value(self,'verse_num')

                    with ui.row() as self.flashcard_container:
                        self.reset_flashcard_view(chapter_num=1,verse_num=1)

                
                            
