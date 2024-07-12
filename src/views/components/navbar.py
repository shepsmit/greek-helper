from contextlib import contextmanager
from nicegui import ui


@contextmanager
def navbar(navigation_title: str, system):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#48bf53', secondary='#11823b', accent='#91f086', positive='#53B689')

    with ui.header().props('reveal'):
        ui.button("Cards", on_click=lambda: system.navigate("/parsed"))
        ui.button("Vocab", on_click=lambda: system.navigate("/vocab"))
        ui.button("Ref", on_click=lambda: system.navigate("/reference"))
        ui.button("Songs", on_click=lambda: system.navigate("/songs"))
    with ui.column().classes('w-full items-center'):
        yield