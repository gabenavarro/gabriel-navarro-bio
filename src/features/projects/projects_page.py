from fasthtml.common import *
from monsterui.all import *
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
        Div(style="height: 3rem;"),
        H1("BLOGS", cls="factory-title", style="margin-bottom: 0;"),
        H1("& MORE", cls="factory-title", style="margin-top: 0;"),
        Div(style="margin-top: 3rem;"),
        Grid(
            *[
                render_project_card(num_projects - i - 1, p)
                for i, p in enumerate(projects)
            ],
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
            style="font-weight: 700; color: var(--color-accent-100); font-size: 0.75rem; border-bottom: 1px solid var(--color-base-900); padding-bottom: 1rem; margin-bottom: 2.5rem; letter-spacing: 0.05em;",
        ),
        Div(
            render_md(project.body),
            cls="factory-markdown-content",
            style="font-size: 1rem; color: var(--color-base-300); line-height: 1.8;",
        ),
        Div(
            A(
                "← RETURN TO SYSTEMS",
                href="/projects",
                cls="factory-accent",
                style="font-weight: 700; font-size: 0.75rem; text-decoration: none; letter-spacing: 0.05em;",
            ),
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
            Div(cls="mt-12")(A("BACK TO HOME", href="/", cls="factory-btn-primary")),
        ),
    )


PROJECTS_PAGE = projects_landing_page()
