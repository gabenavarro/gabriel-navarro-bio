from fasthtml.common import *
from monsterui.all import *


def navigation(logo: str = "GABRIEL"):
    """Returns the Factory-style navigation bar."""
    return NavBar(
        DivRAligned(
            Ul(
                Li(A("Projects", href="/projects", cls="factory-nav-link")),
                Li(A("Blogs", href="/blogs", cls="factory-nav-link")),
                Li(A("CV", href="/cv", cls="factory-nav-link")),
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
    )
