from fasthtml.common import fast_app, serve, Title, Main, database
from src.pages import HERO_PAGE, MASONRY_PAGE, create_blog_page
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

@rt("/projects/{blog_id}")
def get(blog_id: str):
    return Title("Gabriel - Projects"), create_blog_page(blog_id)

serve(port=8080, reload=False)