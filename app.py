from fasthtml.common import fast_app, serve
from src.pages import HERO_PAGE, MASONRY_PAGE

app, rt = fast_app()

@rt("/")
def get():
    return HERO_PAGE

@rt("/projects")
def projects():
    return MASONRY_PAGE

serve(port=8080, reload=False)