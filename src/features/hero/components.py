from fasthtml.common import *
from monsterui.all import *
from src.config import settings


def hero_section():
    """Renders the main hero section of the landing page."""
    content = settings.HERO_CONTENT

    return Section(
        Div(style="height: 3rem;"),
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
                        cls="factory-portrait",
                        style="""
                        width: 100%;
                        max-width: 400px;
                        height: auto;
                        filter: grayscale(100%);
                        transition: all 0.5s ease;
                        display: block;
                        margin: 0 auto;
                        object-fit: contain;
                    """,
                        onmouseover="this.style.filter='grayscale(0%)'; this.style.borderColor='var(--color-accent-100)'",
                        onmouseout="this.style.filter='grayscale(100%)'; this.style.borderColor='var(--color-base-900)'",
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
        Div(style="height: 3rem;"),
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
    return Div(
        # Label with number
        Div(f"{idx + 1:02d} / {data['title'].upper()}", cls="factory-label"),
        # Items/Content
        *[
            Div(
                P(
                    item["subtitle"].upper(),
                    style="font-weight: 700; font-size: 0.875rem; color: var(--color-white); margin-bottom: 0.5rem;",
                ),
                P(
                    *format_text(item["text"]),
                    style="font-size: 0.875rem; color: var(--color-base-400); margin-top: 0; margin-bottom: 1.5rem; line-height: 1.6;",
                ),
            )
            for item in data.get("items", [])
        ],
        # Subsections (nested)
        *[
            Div(
                P(
                    sub["title"].upper(),
                    style="font-weight: 700; font-size: 0.75rem; color: var(--color-base-500); border-bottom: 1px solid var(--color-base-900); padding-bottom: 0.5rem; margin-bottom: 1rem; letter-spacing: 0.05em;",
                ),
                *[
                    P(
                        *format_text(item["text"]),
                        style="font-size: 0.875rem; color: var(--color-base-400); margin-bottom: 1rem; line-height: 1.6;",
                    )
                    for item in sub.get("items", [])
                ],
            )
            for sub in data.get("subsections", [])
        ],
        # Action
        Div(
            A(
                data["button"]["text"].upper() + " ↗",
                href=data["button"]["href"],
                cls="factory-accent",
                style="font-weight: 700; font-size: 0.75rem; text-decoration: none; letter-spacing: 0.05em;",
            ),
            cls="uk-margin-top",
        )
        if "button" in data
        else None,
        style="padding: 2rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary);",
    )


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
