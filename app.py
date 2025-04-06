from fasthtml.common import fast_app, serve
from src.pages import HERO_PAGE, GENOMICS_PROJECT
app, rt = fast_app()

@rt("/")
def get():
    return HERO_PAGE

@rt("/projects")
def projects():
    return GENOMICS_PROJECT

serve(port=80)