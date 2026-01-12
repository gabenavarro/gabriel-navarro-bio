from fasthtml.common import *
from monsterui.all import *
from src.components import StandardPage
from src.services.projects import ProjectService


def render_project_card(idx, project):
    """Renders a project as a Factory technical card."""
    return Div(
        A(
            # Category Label
            Div(
                f"{idx + 1:02d} / {' / '.join(project.tags).upper()}",
                cls="factory-label",
            ),
            # Project Image
            Img(
                src=project.image,
                alt=project.title,
                style="width: 100%; height: 200px; object-fit: cover; border: 1px solid var(--color-base-900); border-radius: var(--radius-md); margin-bottom: 1rem; filter: grayscale(100%); transition: filter 0.3s ease;",
                onmouseover="this.style.filter='grayscale(0%)'",
                onmouseout="this.style.filter='grayscale(100%)'",
            )
            if project.image
            else None,
            # Title and Description
            H3(
                project.title.upper(),
                style="font-size: 1.25rem; font-weight: 700; color: var(--color-white); margin-top: 0; margin-bottom: 0.5rem;",
            ),
            P(
                project.description,
                style="font-size: 0.875rem; color: var(--color-base-400); line-height: 1.6;",
            ),
            href=f"/blogs/{project.id}",
            style="text-decoration: none; color: inherit; display: block;",
        ),
        style="padding: 1.5rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary); transition: border-color 0.3s ease;",
        cls="uk-transition-target",
    )


def create_masonry_page(tag: str | None = None):
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
