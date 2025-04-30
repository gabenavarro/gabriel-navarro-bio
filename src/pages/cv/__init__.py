from src.pages.cv.cv_body import CV_CSS, cv_contact, cv_education, cv_experience, cv_skills, cv_patents, cv_publications
from src.lib.css import ROOT_CSS, BODY_CSS
from src.components import simple_navigation, contact_me_modal
from fasthtml.common import Style, Div

CV_PAGE = Div(
    Style(ROOT_CSS + BODY_CSS + CV_CSS),
    simple_navigation(),
    Div("Curriculum Vitae", cls="highlight title banner-title-spacing"),
    cv_experience(),
    cv_education(),
    cv_skills(),
    cv_patents(),
    cv_publications(),
    contact_me_modal(),
    cls="container",
)