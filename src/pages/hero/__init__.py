from fasthtml.common import Style, Div, Script
from src.components import simple_navigation, contact_me_modal
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import SCROLL_JS
from src.pages.hero.hero_section import HERO_SECTION
from src.components.backgrounds import VERTICAL_LINE
from src.pages.hero.about_section import ABOUT_ME

HERO_PAGE = Div(
    Style(ROOT_CSS + BODY_CSS),
    Script(SCROLL_JS),
    simple_navigation(),
    VERTICAL_LINE,
    HERO_SECTION,
    ABOUT_ME,
    contact_me_modal(),
)