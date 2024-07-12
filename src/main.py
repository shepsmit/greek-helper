from nicegui import ui

from backend.system import FlashCardSet
from views.parsed import ViewParsed
from views.reference import ViewReference
from views.songs import ViewSongs
from views.vocab import ViewVocab

# Initialize all the app pages
system = FlashCardSet()

flashcardView = ViewParsed(system)
vocabView = ViewVocab(system)
referenceView = ViewReference()
songsView = ViewSongs()


## Start up the UI
# ui.run(host="0.0.0.0",port=80, title='Greek Helper')
ui.run(port=8080, title='Greek Helper')

ui.navigate.to("/parsed")