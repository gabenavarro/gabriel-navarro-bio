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

    projects = projects[::-1]
    num_projects = len(projects)

    content = [
        Div(cls="page-spacer-md"),
        H1("BLOGS", cls="factory-title factory-title-tight-bottom"),
        H1("& MORE", cls="factory-title factory-title-tight-top"),
        Div(cls="projects-grid-spacer"),
        Grid(
            *[render_project_card(num_projects - i - 1, p) for i, p in enumerate(projects)],
            cols_min=1,
            cols_sm=1,
            cols_md=2,
            cols_lg=3,
            cls="gap-8",
        ),
    ]

    return StandardPage("Projects", *content)


def create_blog_page(uuid: str):
    """Creates a detail page for a specific blog post."""
    service = ProjectService()
    project = service.get_project_by_id(uuid)

    if not project:
        return StandardPage("Not Found", H1("PROJECT NOT FOUND", cls="factory-title"))

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
