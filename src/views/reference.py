
from nicegui import ui
from views.components.navbar import navbar

class ViewReference():
    def __init__(self):
        self.setupView()
    
    def setupView(self):
        @ui.page('/reference')
        def page_index():
            with navbar('Reference', self.system):
                ### Header ###
                with ui.row().classes('w-full items-center'):
                    ui.image("src/images/ref/article.png").classes("w-1/3")
                    ui.image("src/images/ref/pronouns_1_2.png").classes("w-1/4")
                    ui.image("src/images/ref/pronouns_3.png").classes("w-1/4")
                    ui.image("src/images/ref/relative_pronoun.png").classes("w-1/4")
                    ui.image("src/images/ref/pronouns_near.png").classes("w-1/4")
                    ui.image("src/images/ref/pronouns_far.png").classes("w-1/4")
                    ui.image("src/images/ref/Tenses.png").classes("w-1/2")
                    ui.image("src/images/ref/Indicative.png").classes("w-1/2")
                    ui.image("src/images/ref/Subjunctive.png").classes("w-1/2")
                    ui.image("src/images/ref/Participles.png").classes("w-1/2")
                    ui.image("src/images/ref/Infinitives.png").classes("w-1/2")
                    ui.image("src/images/ref/Imperative.png").classes("w-1/2")

                
                            
