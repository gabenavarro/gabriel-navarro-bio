from fasthtml.common import *
from monsterui.all import *
from src.pages.cv.cv_body import (
    cv_experience,
    cv_education,
    cv_skills,
    cv_patents,
    cv_publications,
)
from src.components import StandardPage

CV_PAGE = StandardPage(
    "Gabriel - CV",
    Div(cls="underline"),
    Div(style="height: 3rem;"),
    H1("CURRICULUM", cls="factory-title", style="margin-bottom: 0;"),
    H1("VITAE", cls="factory-title", style="margin-bottom: 0;"),
    cv_experience(),
    Div(style="height: 3rem;"),
    cv_education(),
    Div(style="height: 3rem;"),
    cv_skills(),
    Div(style="height: 3rem;"),
    cv_patents(),
    Div(style="height: 3rem;"),
    cv_publications(),
)
