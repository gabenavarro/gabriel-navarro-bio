from fasthtml.common import *
from monsterui.all import *

from src.config.settings import settings


def navigation(logo: str = "GABRIEL"):
    """Returns the Factory-style navigation bar.

    Passes nav links as positional `A(...)` items per MonsterUI's documented
    `NavBar(*c, brand=...)` API. The previous `Ul(Li(A(...)), cls="uk-navbar-nav")`
    pattern was an old UIkit-3 idiom that FrankenUI 2 (MonsterUI's underlying
    CSS framework) dropped: the `.uk-navbar-nav` class is a no-op there, so
    Tailwind's preflight reset left the UL as `display: block`, stacking the
    links into a 61px-wide vertical column at the right edge of the viewport.
    """
    return NavBar(
        *[
            A(link["label"], href=link["href"], cls="factory-nav-link")
            for link in settings.NAV_LINKS
        ],
        brand=DivLAligned(
            A(
                logo,
                href="/",
                cls="uk-navbar-item uk-logo factory-brand",
            ),
        ),
        sticky=True,
        cls="factory-nav",
        aria_label="Primary navigation",
    )
