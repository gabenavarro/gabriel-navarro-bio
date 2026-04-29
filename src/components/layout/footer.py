"""Site footer rendered on every page below the main container."""

from datetime import datetime

from fasthtml.common import A, Div, P

from src.config.settings import settings


def Footer():
    """Render the site footer.

    Reads link lists from `settings.NAV_LINKS` and `settings.SOCIAL_LINKS`
    so the navigation, social buttons, and footer share a single source of
    truth. Outputs Factory-style monochrome markup that mirrors the navbar.
    """
    year = datetime.now().year
    return Div(
        Div(
            Div(
                P("GABRIEL", cls="factory-footer-brand"),
                P(
                    "Computational biology × foundation models",
                    cls="factory-footer-tagline",
                ),
                cls="factory-footer-col",
            ),
            Div(
                *[
                    A(
                        link["label"],
                        href=link["href"],
                        cls="factory-footer-link",
                        target="_blank" if link["href"].startswith("http") else None,
                        rel="noopener noreferrer" if link["href"].startswith("http") else None,
                    )
                    for link in settings.SOCIAL_LINKS
                ],
                # NOTE: was `factory-footer-col factory-footer-row` — both classes
                # set `display: flex` but col forces `flex-direction: column`,
                # which won the cascade and stacked the social links vertically.
                # Drop the col class so the row's default horizontal layout wins.
                cls="factory-footer-row",
                aria_label="Social links",
            ),
            cls="factory-footer-row",
        ),
        Div(cls="factory-footer-divider"),
        Div(
            P(f"© {year} Gabriel Navarro", cls="factory-footer-copyright"),
            Div(
                *[
                    A(link["label"], href=link["href"], cls="factory-footer-link")
                    for link in settings.NAV_LINKS
                ],
                cls="factory-footer-row",
                aria_label="Footer navigation",
            ),
            cls="factory-footer-row",
        ),
        cls="factory-footer",
    )
