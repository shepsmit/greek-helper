
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

def getFlashCardParsing(flashcard: FlashCard):
    with ui.row():
        if flashcard.number != None:
            match flashcard.number:
                case Number.SINGULAR:
                    ui.icon('person')
                case Number.PLURAL:
                    ui.icon('groups')
        if flashcard.person != None:
            match flashcard.person:
                case Person.FIRST:
                    ui.label('1')
                case Person.SECOND:
                    ui.label('2')
                case Person.THIRD:
                    ui.label('3')

class FlashCardContainer(ui.card):
    def __init__(self, flashcard: FlashCard, class_str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._side = FlashCardSide.FRONT
        self.flashcard = flashcard
        self.on('click', self.toggle)

        self.class_str = class_str

        with self: # default for front
            getFlashCardElement(self.flashcard, self._side, self.class_str)
            getFlashCardParsing(self.flashcard)


    def toggle(self) -> None:
        """Toggle the container state."""
        if(self._side == FlashCardSide.FRONT):
            self._side = FlashCardSide.BACK
        else:
            self._side = FlashCardSide.FRONT
        self.clear()
        with self:
            c = getFlashCardElement(self.flashcard, self._side, self.class_str)
            p = getFlashCardParsing(self.flashcard)
            c.update()
            p.update()

        self.update()

    def update(self) -> None:
        # Code here during updates
        super().update()

class ViewFlashCard():
    def __init__(self):
        self.setupView()
    
    def load_flashcards(self):
        fset = FlashCardSet("1 John 1")
        f_cards = fset.get_flashcard_set_verse_words(verse_num=1)

        for f in f_cards[:100]:
            card_class_str = "items-center"
            if(f.gender != None):
                match f.gender:
                    case Gender.FEMININE:
                        card_class_str += " border-red-700"
                    case Gender.MASCULINE:
                        card_class_str += " border-blue-700"
                    case Gender.NEUTER:
                        card_class_str += " border-black-700"
                card_class_str += " border-2 border-solid"
            
            # match f.number:
            #     case Number.PLURAL:
            #         card_class_str += " shadow-lg shadow-orange-900"
            #     case Number.SINGULAR:
            #         card_class_str += " shadow-none"
            #     case None:
            #         card_class_str += " shadow-none"

            with ui.card().classes(card_class_str):
                FlashCardContainer(flashcard=f, class_str="w-24 h-24 text-center")


    def setupView(self):
        @ui.page('/')
        def page_index():
            with navbar('Session In Progress'):
                ### Header ###
                with ui.row().classes('w-full items-center') as content:
                    self.load_flashcards()

                
                            
