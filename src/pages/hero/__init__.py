from fasthtml.common import Style, Div
from src.components import NAVIGATION
from src.components.backgrounds import GRADIENT_TRANSITION
from src.styles import ROOT_CSS, BODY_CSS
from src.pages.hero.hero_section import HERO_SECTION as _hero_section
from src.pages.hero.about_section import ABOUT_SECTION as _about_section

HERO_PAGE = Div(
    Style(ROOT_CSS + BODY_CSS),
    NAVIGATION,
    _hero_section,
    GRADIENT_TRANSITION,
    _about_section
)