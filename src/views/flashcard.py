
from nicegui import ui
from backend.system import FlashcardSet
from models.utils import FlashCard, FlashCardSide, FlashCardContent
from views.components.navbar import navbar

def getFlashCardElement(flashcard: FlashCard, side:FlashCardSide):
    if(side == FlashCardSide.FRONT):
        if(flashcard.front_type == FlashCardContent.IMAGE):
            return (ui.image(flashcard.front).classes('w-16'))
        elif(flashcard.front_type == FlashCardContent.TEXT):
            return (ui.label(flashcard.front))
    
    if(side == FlashCardSide.BACK):
        if(flashcard.back_type == FlashCardContent.IMAGE):
            return (ui.image(flashcard.back).classes('w-16'))
        elif(flashcard.back_type == FlashCardContent.TEXT):
            return (ui.label(flashcard.back))

class FlashCardButton(ui.button):
    def __init__(self, container, flashcard: FlashCard, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state = False
        self.container = container
        self.flashcard = flashcard
        self.on('click', self.toggle)

    def toggle(self) -> None:
        """Toggle the button state."""
        self._state = not self._state
        self.container.clear()
        with self.container:
            if(self._state):
                c = getFlashCardElement(self.flashcard, FlashCardSide.FRONT)
                c.update()
            else:
                c = getFlashCardElement(self.flashcard, FlashCardSide.BACK)
                c.update()

        self.update()

    def update(self) -> None:
        self.props(f'color={"green" if self._state else "red"}')
        super().update()



class ViewFlashCard():
    def __init__(self):


        self.setupView()
    
    def loadFlashcards(self):
        fset = FlashcardSet()
        fset.loadFlashcardSet()

        for flashcard in fset.flashcards[:10]:
            with ui.card():
                container = ui.row()
                with container:
                    print(flashcard.front)
                    ui.image(flashcard.front).classes('w-16')

                FlashCardButton(container=container, flashcard=flashcard)


    def setupView(self):
        @ui.page('/')
        def page_index():
            with navbar('Session In Progress'):
                ### Header ###
                with ui.row().classes('w-full items-center') as content:
                    self.loadFlashcards()

                
                            
