from fasthtml.common import *
from fasthtml.common import Title as TitleTag
from monsterui.all import *
from src.components import simple_navigation, contact_me_modal
from src.styles.factory import FACTORY_CSS

def StandardPage(title: str, *content, extra_styles: str = "", extra_scripts=None, cls=""):
    """
    Standard page wrapper with navigation, contact modal, and Factory theme.
    """
    scripts = extra_scripts if extra_scripts else []
    if not isinstance(scripts, list):
        scripts = [scripts]
        
    return (
        Head(
            Title(title),
            # Geist Font Import (Heuristic - assuming it's available or using system fallback in CSS)
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/sans.css"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/mono.css"),
        ),
        Style(FACTORY_CSS + extra_styles),
        *scripts,
        simple_navigation(),
        Container(
            Section(
                *content,
                cls=cls
            ),
            cls="uk-container-large" # Use larger container for technical layout
        ),
        # contact_me_modal() # Modal needs refactoring for MonsterUI, disabling for now
    )
