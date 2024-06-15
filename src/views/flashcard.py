
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
    
    def load_parsed_icons(self, f:FlashCard):
        if(f.tense != None):
            match f.tense:
                case Tense.PRESENT:
                    ui.image("src/images/icons/tense_present.png").classes("w-6 h-6")
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

    def load_flash_cards(self, f_cards:list):
        for f in f_cards[:100]:
            card_class_str = "items-center"
            with ui.card().classes(card_class_str):
                FlashCardContainer(flashcard=f, class_str="w-24 h-24 text-center")
                # Now put the parsing info below the image
                with ui.row().classes("items-center"):
                    self.load_parsed_icons(f)
    

    def load_flashcard_view(self):
        chapter_ref = "1 John 1"
        fset = FlashCardSet(chapter_ref)
        ui.label(chapter_ref)

        # ui.number(label='Verse', value=1,
        #   on_change=lambda e: self.update_flashcards(e.value))

        f_cards = fset.get_flashcard_set_verse_words(verse_num=1)
        self.load_flash_cards(f_cards)

        
                    


    def setupView(self):
        @ui.page('/')
        def page_index():
            with navbar('Session In Progress'):
                ### Header ###
                with ui.row().classes('w-full items-center') as content:
                    self.load_flashcard_view()

                
                            
