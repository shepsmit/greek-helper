from nicegui import ui

from views.flashcard import ViewFlashCard

# Initialize all the app pages
flashcardView = ViewFlashCard()

## Start up the UI
ui.run(port=8080, title='Greek Helper')