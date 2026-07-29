from fasthtml.common import *
from monsterui.all import *

from src.components.layout.page import StandardPage

from .components import (
    cv_education,
    cv_experience,
    cv_patents,
    cv_publications,
    cv_skills,
)

CV_PAGE = StandardPage(
    "Gabriel - CV",
    Div(cls="underline"),
    Div(cls="page-spacer-md"),
    H1("CURRICULUM", cls="factory-title factory-title-tight-bottom"),
    H1("VITAE", cls="factory-title factory-title-tight-bottom"),
    cv_experience(),
    Div(cls="page-spacer-md"),
    cv_education(),
    Div(cls="page-spacer-md"),
    cv_skills(),
    Div(cls="page-spacer-md"),
    cv_patents(),
    Div(cls="page-spacer-md"),
    cv_publications(),
)
