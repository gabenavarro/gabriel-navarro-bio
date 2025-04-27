from fasthtml.common import fast_app, serve, Title, Main, database
from src.pages import HERO_PAGE, MASONRY_PAGE

# This is a simple FastHTML app that serves a page with a title and a main content area.
app, rt = fast_app()

# Main page
@rt("/")
def get():
    return Title("Gabriel"), Main(HERO_PAGE)

# Projects page
@rt("/projects")
def projects():
    return Title("Gabriel - Projects"), MASONRY_PAGE


serve(port=8080, reload=False)