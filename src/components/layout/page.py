from fasthtml.common import *
from monsterui.all import *
from .navigation import navigation
from src.styles import FACTORY_CSS, THEME_CSS


def StandardPage(
    title: str, *content, extra_styles: str = "", extra_scripts=None, cls=""
):
    """
    Standard page wrapper with navigation and Factory theme.
    """
    scripts = extra_scripts if extra_scripts else []
    if not isinstance(scripts, list):
        scripts = [scripts]

    return (
        Head(
            Title(title),
            # Geist Font Import
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/sans.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/mono.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@fontsource/cascadia-mono@5.2.3/index.min.css",
            ),
        ),
        Style(THEME_CSS + FACTORY_CSS + extra_styles),
        *scripts,
        navigation(),
        Container(
            Section(*content, cls=cls),
            cls="uk-container-large",
        ),
    )
