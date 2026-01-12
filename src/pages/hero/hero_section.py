from fasthtml.common import *
from monsterui.all import *
from src.config import settings


def hero_section():
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


HERO_SECTION = hero_section()
