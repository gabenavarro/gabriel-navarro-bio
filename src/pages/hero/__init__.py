from fasthtml.common import Style, Div, Script
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import SCROLL_JS
from src.pages.hero.hero_section import HERO_SECTION
from src.components.backgrounds import VERTICAL_LINE
from src.pages.hero.about_section import ABOUT_ME

HERO_PAGE = Div(
    Style(ROOT_CSS + BODY_CSS),
    Script(SCROLL_JS),
    NAVIGATION,
    HERO_SECTION,
    VERTICAL_LINE,
    ABOUT_ME
)