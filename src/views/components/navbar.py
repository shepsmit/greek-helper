from contextlib import contextmanager
from nicegui import ui


@contextmanager
def navbar(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#48bf53', secondary='#11823b', accent='#91f086', positive='#53B689')
    with ui.header().props('reveal'):
        ui.button("Cards", on_click=lambda: ui.navigate.to("/"))
        ui.button("Ref", on_click=lambda: ui.navigate.to("/reference"))
        ui.button("Songs", on_click=lambda: ui.navigate.to("/songs"))
    with ui.column().classes('w-full items-center'):
        yield