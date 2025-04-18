from fasthtml.common import fast_app, serve, Title, Main
from src.pages import HERO_PAGE, MASONRY_PAGE


app, rt = fast_app()

@rt("/")
def get():
    return Title("Gabriel"), Main(HERO_PAGE)

@rt("/projects")
def projects():
    return Title("Gabriel - Projects"), MASONRY_PAGE


serve(port=8080, reload=False)