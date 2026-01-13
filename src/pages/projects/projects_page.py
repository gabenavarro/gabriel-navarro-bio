from fasthtml.common import *
from monsterui.all import *
from src.components import StandardPage


def projects_page():
    return StandardPage(
        "PROJECTS",
        DivCentered(cls="uk-section-large")(
            Div(cls="factory-label")("PROJECTS"),
            H1("UNDER CONSTRUCTION", cls="factory-title"),
            P(
                "I'm currently building something great. Check back soon for my latest work and case studies.",
                cls="factory-sub",
            ),
            Div(cls="mt-12")(A("BACK TO HOME", href="/", cls="factory-btn-primary")),
        ),
    )


PROJECTS_PAGE = projects_page()
