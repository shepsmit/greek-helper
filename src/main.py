from nicegui import ui

from backend.system import FlashCardSet
from views.flashcard import ViewFlashCard
from views.reference import ViewReference
from views.songs import ViewSongs

# Initialize all the app pages
system = FlashCardSet()

flashcardView = ViewFlashCard(system)
referenceView = ViewReference()
songsView = ViewSongs()

## Start up the UI
ui.run(port=8080, title='Greek Helper')