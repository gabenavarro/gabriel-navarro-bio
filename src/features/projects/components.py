from fasthtml.common import *
from monsterui.all import *


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
