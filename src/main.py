from nicegui import ui

from views.flashcard import ViewFlashCard
from views.reference import ViewReference
from views.songs import ViewSongs

# Initialize all the app pages
flashcardView = ViewFlashCard()
referenceView = ViewReference()
songsView = ViewSongs()

## Start up the UI
ui.run(port=8080, title='Greek Helper')