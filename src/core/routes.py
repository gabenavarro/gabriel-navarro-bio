from fasthtml.common import *
from src.features.hero import HERO_PAGE
from src.features.projects import PROJECTS_PAGE, create_masonry_page, create_blog_page
from src.features.cv import CV_PAGE


def register_routes(app, rt):
    """
    Registers all application routes.
    """

    @rt("/")
    def get():
        return HERO_PAGE

    @rt("/projects")
    def projects(tag: str = None):
        return PROJECTS_PAGE

    @rt("/blogs")
    def blogs(tag: str = None):
        return create_masonry_page(tag)

    @rt("/blogs/{blog_id}")
    def get_blog(blog_id: str):
        return create_blog_page(blog_id)

    @rt("/cv")
    def cv():
        return CV_PAGE
