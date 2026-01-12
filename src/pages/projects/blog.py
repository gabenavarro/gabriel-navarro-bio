from fasthtml.common import *
from monsterui.all import *
from src.components import StandardPage
from src.services.projects import ProjectService


def create_blog_page(uuid: str):
    """Create a Factory-style project detail page."""
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
        # Featured Image
        # TODO: Review blogs and make sure not double displaying
        # Img(
        #     src=project.image,
        #     style="width: 100%; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); margin-bottom: 3rem; filter: grayscale(100%); transition: filter 0.5s ease;",
        #     onmouseover="this.style.filter='grayscale(0%)'",
        #     onmouseout="this.style.filter='grayscale(100%)'"
        # )
        # if project.image
        # else None,
        # Project Content
        Div(
            render_md(project.body),
            cls="factory-markdown-content",
            style="font-size: 1rem; color: var(--color-base-300); line-height: 1.8;",
        ),
        # Back Link
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

    return StandardPage(project.title, *content)
