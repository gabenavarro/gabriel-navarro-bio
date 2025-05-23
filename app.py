from fasthtml.common import fast_app, serve, Title, Main
from src.pages import HERO_PAGE, create_masonry_page, CV_PAGE, create_blog_page
import argparse

# This is a simple FastHTML app that serves a page with a title and a main content area.
app, rt = fast_app()

# Main page
@rt("/")
def get():
    return Title("Gabriel"), Main(HERO_PAGE)

# Projects page
@rt("/projects")
def projects(tag: str = None):
    """
    Projects page with a masonry layout and filter chips.
    ### Args:
        - tag (str): Optional tag to filter projects by. ?tag=machine-learning, etc.
    ### Returns:
        - Title: Page title.
        - Div: Main content of the page.
    """
    return Title("Gabriel - Projects"), create_masonry_page(tag)

@rt("/projects/{blog_id}")
def get_project(blog_id: str):
    return Title("Gabriel - Projects"), create_blog_page(blog_id)

# CV page
@rt("/cv")
def cv():
    return Title("Gabriel - CV"), CV_PAGE

# Parse command line argument for port
parser = argparse.ArgumentParser(description="Run the FastHTML app.")
parser.add_argument("--port", type=int, default=80, help="Port to run the app on")
args = parser.parse_args()

serve(port=args.port, reload=False)