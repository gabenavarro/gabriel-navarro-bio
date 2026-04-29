from fasthtml.common import *
from starlette.responses import Response

from src.features.hero import HERO_PAGE
from src.features.projects import (
    PROJECTS_PAGE,
    create_blog_page,
    create_blog_page_by_slug,
    create_masonry_page,
)
from src.features.cv import CV_PAGE
from src.features.feed.rss import build_rss_feed
from src.services.projects import ProjectService


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

    @rt("/blogs/slug/{slug}")
    def get_blog_by_slug(slug: str):
        return create_blog_page_by_slug(slug)

    @rt("/blogs/{blog_id}")
    def get_blog(blog_id: str):
        return create_blog_page(blog_id)

    @rt("/cv")
    def cv():
        return CV_PAGE

    @rt("/feed.xml")
    def feed_xml():
        service = ProjectService()
        projects = service.get_all_projects(limit=50, include_disabled=False)
        body = build_rss_feed(projects)
        return Response(body, media_type="application/rss+xml")

    # FastHTML's `fast_app` registers a static-asset catch-all
    # `/{fname:path}.{ext:static}` *before* user routes, and `xml` is one of
    # its recognized static extensions. Without reordering, /feed.xml is
    # claimed by the static handler and 404s (no file on disk). Move our
    # explicit /feed.xml route to the front so Starlette matches it first.
    feed_routes = [r for r in app.router.routes if getattr(r, "path", None) == "/feed.xml"]
    other_routes = [r for r in app.router.routes if getattr(r, "path", None) != "/feed.xml"]
    app.router.routes[:] = feed_routes + other_routes
