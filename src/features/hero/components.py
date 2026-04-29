from fasthtml.common import *
from monsterui.all import *
from src.components.base import Card, button_ghost
from src.config import settings


def hero_section():
    """Renders the main hero section of the landing page."""
    content = settings.HERO_CONTENT

    return Section(
        Div(cls="page-spacer-md"),
        Grid(
            # Typography
            Div(
                H1(
                    content["greeting"].upper(),
                    cls="factory-title",
                ),
                Div(
                    render_md(content["default_description"]),
                    cls="factory-sub",
                ),
            ),
            # Portrait
            A(
                Div(
                    Img(
                        src=content["portrait_url"],
                        alt="Gabriel Navarro",
                        cls="factory-portrait hero-portrait-img",
                    ),
                    cls="uk-flex uk-flex-center uk-flex-middle",
                ),
                href="https://www.linkedin.com/in/gcnavarro/",
                target="_blank",
                cls="factory-portrait",
            ),
            cols_min=1,
            cols_md=2,
            cls="uk-grid-large uk-flex-middle",
        ),
        Div(cls="page-spacer-md"),
        cls="uk-section-large",
    )


def format_text(text):
    """Simple markdown-like formatter for bold text."""
    import re

    parts = re.split(r"(\*\*.*?\*\*)", text)
    result = []
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            result.append(Strong(part[2:-2]))
        else:
            result.append(part)
    return result


def render_principle(idx, data):
    """Renders a section as a Factory technical block."""
    children = [
        Div(f"{idx + 1:02d} / {data['title'].upper()}", cls="factory-label"),
    ]

    for item in data.get("items", []):
        children.append(
            Div(
                P(item["subtitle"].upper(), cls="principle-item-title"),
                P(*format_text(item["text"]), cls="principle-item-body"),
            )
        )

    for sub in data.get("subsections", []):
        children.append(
            Div(
                P(sub["title"].upper(), cls="principle-subsection-title"),
                *[
                    P(*format_text(item["text"]), cls="principle-subsection-body")
                    for item in sub.get("items", [])
                ],
            )
        )

    if "button" in data:
        children.append(
            Div(
                button_ghost(
                    data["button"]["text"].upper() + " ↗",
                    href=data["button"]["href"],
                ),
                cls="uk-margin-top",
            )
        )

    return Card(*children, padding="lg")


def about_section():
    """Renders the about section with multiple principle blocks."""
    sections = settings.HERO_CONTENT["about_sections"]

    return Section(
        Div(
            Grid(
                *[render_principle(i, sec) for i, sec in enumerate(sections)],
                cols_min=1,
                cols_sm=1,
                cols_md=2,
                cols_lg=3,
                cls="rams-grid",
            )
        ),
        cls="uk-section-large",
    )
