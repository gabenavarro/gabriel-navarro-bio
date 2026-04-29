from fasthtml.common import *
from monsterui.all import *

from src.config.settings import settings


def navigation(logo: str = "GABRIEL"):
    """Returns the Factory-style navigation bar."""
    return NavBar(
        DivRAligned(
            Ul(
                *[
                    Li(A(link["label"], href=link["href"], cls="factory-nav-link"))
                    for link in settings.NAV_LINKS
                ],
                cls="uk-navbar-nav uk-visible@m",
            ),
        ),
        brand=DivLAligned(
            A(
                logo,
                href="/",
                cls="uk-navbar-item uk-logo",
                style="font-family: 'Geist', sans-serif; font-weight: 900; letter-spacing: -0.05em; color: #FFFFFF;",
            ),
        ),
        sticky=True,
        cls="factory-nav",
        aria_label="Primary navigation",
    )
