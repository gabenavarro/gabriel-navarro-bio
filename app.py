from fasthtml.common import *
from monsterui.all import *
from src.pages import (
    HERO_PAGE,
    create_masonry_page,
    CV_PAGE,
    create_blog_page,
    PROJECTS_PAGE,
)
import argparse

# This is a simple FastHTML app that serves a page with a title and a main content area.
app, rt = fast_app(
    hdrs=(
        Theme.slate.headers(highlightjs=True),
        Favicon(
            "/assets/ico/favicon.ico",
            "/assets/ico/favicon.ico"
        ),
    ),
    title="Gabriel, PhD",
)


# Main page
@rt("/")
def get():
    return HERO_PAGE


# Projects page
@rt("/projects")
def projects(tag: str = None):
    return PROJECTS_PAGE


# Blogs page
@rt("/blogs")
def blogs(tag: str = None):
    return create_masonry_page(tag)


@rt("/blogs/{blog_id}")
def get_blog(blog_id: str):
    return create_blog_page(blog_id)


# CV page
@rt("/cv")
def cv():
    return CV_PAGE


# Parse command line argument for port
parser = argparse.ArgumentParser(description="Run the FastHTML app.")
parser.add_argument("--port", type=int, default=80, help="Port to run the app on")
args = parser.parse_args()

serve(port=args.port, reload=False)
