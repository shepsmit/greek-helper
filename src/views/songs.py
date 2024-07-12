
from nicegui import ui
from views.components.navbar import navbar

class ViewSongs():
    def __init__(self):
        self.setupView()
    
    def setupView(self):
        @ui.page('/songs')
        def page_index():
            with navbar('Songs', self.system):
                ### Header ###
                with ui.row().classes('w-full'):
                    with ui.card():
                        ui.label("Intro")
                        ui.link("Alphabet","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=1",new_tab=True)
                        ui.link("Article","https://youtu.be/h_1V8BL5MUg?list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&t=18",new_tab=True)
                    
                    with ui.card():
                        ui.label("Nouns")
                        ui.link("1st Declension","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=2",new_tab=True)
                        ui.link("2nd Declension","https://www.youtube.com/watch?v=EBYeerWcB9c&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=3",new_tab=True)
                        ui.link("3rd Declension","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=4",new_tab=True)
                    with ui.card():
                        ui.label("Verbs")
                        ui.link("Present Active Indicative","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=6",new_tab=True)
                        ui.link("Present Middle & Passive","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=7",new_tab=True)
                        ui.link("Future Active and Middle","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=8",new_tab=True)
                        ui.link("Imperfect Indicative & Secondary Endings","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=9",new_tab=True)
                        ui.link("Aorist Active and Middle","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=10",new_tab=True)
                    with ui.card():
                        ui.label("Verbs")
                        ui.link("The Passives","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=11",new_tab=True)
                        ui.link("The PluPerfect Song","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=12",new_tab=True)
                        ui.link("The Liquid Verbs","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=13",new_tab=True)
                        ui.link("The mi Verbs","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=14",new_tab=True)
                        ui.link("The Subjunctive","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=15",new_tab=True)
                        ui.link("The Imperative","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=16",new_tab=True)
                        ui.link("The Infinitives","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=17",new_tab=True)
                        ui.link("The Participles","https://www.youtube.com/watch?v=UEyns65Zf8s&list=PLO-USksx-puxxltOhjEK-tSEjbEX1XepZ&index=18",new_tab=True)
                
                            
