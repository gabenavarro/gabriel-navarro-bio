from fasthtml.common import *
from monsterui.all import *
from src.components.base import button_ghost, button_primary
from src.components.layout.page import StandardPage
from src.services.projects import ProjectService
from .components import render_project_card


def create_masonry_page(tag: str | None = None):
    """Creates the masonry layout page for blogs/projects."""
    service = ProjectService()
    if tag:
        projects = service.get_projects_by_tag(tag)
    else:
        projects = service.get_all_projects()

    num_projects = len(projects)

    content = [
        Div(cls="page-spacer-md"),
        H1("BLOGS", cls="factory-title factory-title-tight-bottom"),
        H1("& MORE", cls="factory-title factory-title-tight-top"),
        Div(cls="projects-grid-spacer"),
        Div(
            *[render_project_card(num_projects - i - 1, p) for i, p in enumerate(projects)],
            cls="masonry-columns",
        ),
    ]

    return StandardPage("Projects", *content)


def _render_blog_detail(project):
    """Render the shared blog detail body for a Project (UUID or slug lookup)."""
    content = [
        Div("TECHNICAL OVERVIEW", cls="factory-label"),
        H1(project.title.upper(), cls="factory-title"),
        P(
            f"SYSTEM / {' / '.join(project.tags).upper()}",
            cls="blog-detail-meta",
        ),
        Div(
            render_md(project.body),
            cls="factory-markdown-content blog-detail-body",
        ),
        Div(
            button_ghost("← RETURN TO SYSTEMS", href="/projects"),
            cls="uk-margin-large-top",
        ),
    ]

    return StandardPage(project.title, *content)


def create_blog_page(uuid: str):
    """Creates a detail page for a specific blog post (looked up by UUID)."""
    service = ProjectService()
    project = service.get_project_by_id(uuid)

    if not project:
        return StandardPage("Not Found", H1("PROJECT NOT FOUND", cls="factory-title"))

    return _render_blog_detail(project)


def create_blog_page_by_slug(slug: str):
    """Render a blog detail page looked up by slug."""
    service = ProjectService()
    project = service.get_project_by_slug(slug)

    if not project:
        return StandardPage("Not Found", H1("PROJECT NOT FOUND", cls="factory-title"))

    return _render_blog_detail(project)


def projects_landing_page():
    """Returns the projects placeholder page."""
    return StandardPage(
        "PROJECTS",
        DivCentered(cls="uk-section-large")(
            Div(cls="factory-label")("PROJECTS"),
            H1("UNDER CONSTRUCTION", cls="factory-title"),
            P(
                "I'm currently building something great. Check back soon for my latest work and case studies.",
                cls="factory-sub",
            ),
            Div(cls="mt-12")(button_primary("BACK TO HOME", href="/")),
        ),
    )


PROJECTS_PAGE = projects_landing_page()
