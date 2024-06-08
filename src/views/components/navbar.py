from contextlib import contextmanager
from nicegui import ui


@contextmanager
def navbar(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#48bf53', secondary='#11823b', accent='#91f086', positive='#53B689')
    with ui.header():
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('Placeholder', lambda: ui.notify("Hi"))
    with ui.column().classes('w-full items-center'):
        yield