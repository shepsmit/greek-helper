
from nicegui import ui
from backend.system import FlashCardSet
from models.utils import FlashCard, FlashCardSide, FlashCardContent
from views.components.navbar import navbar

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
    
    def loadFlashcards(self):
        fset = FlashCardSet("1 John 1")
        # fset.greek_parser.newLemma("ἀρχή")
        f_cards = fset.getFlashCardSetVerseWords(verse_num=1)

        for f in f_cards[:100]:
            with ui.card().classes('items-center').tight():
                FlashCardContainer(flashcard=f, class_str="w-32 h-32 text-center").tight()


    def setupView(self):
        @ui.page('/')
        def page_index():
            with navbar('Session In Progress'):
                ### Header ###
                with ui.row().classes('w-full items-center') as content:
                    self.loadFlashcards()

                
                            
