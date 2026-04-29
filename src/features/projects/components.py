from fasthtml.common import *
from monsterui.all import *
from src.components.base import Card


def render_project_card(idx, project):
    """Renders a project as a Factory technical card."""
    body = [
        Div(
            f"{idx + 1:02d} / {' / '.join(project.tags).upper()}",
            cls="factory-label",
        ),
    ]
    if project.image:
        body.append(
            Img(
                src=project.image,
                alt=project.title,
                cls="factory-card-image",
            )
        )
    body.append(H3(project.title.upper(), cls="factory-card-title"))
    body.append(P(project.description, cls="factory-card-description"))

    href = f"/blogs/slug/{project.slug}" if project.slug else f"/blogs/{project.id}"

    return Card(
        *body,
        href=href,
        interactive=True,
        padding="md",
    )
