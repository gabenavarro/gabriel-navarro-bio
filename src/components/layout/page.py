from fasthtml.common import *
from monsterui.all import *
from .footer import Footer
from .navigation import navigation
from src.styles import FACTORY_CSS, THEME_CSS


def StandardPage(
    title: str,
    *content,
    extra_styles: str = "",
    extra_scripts=None,
    cls: str = "",
    meta: dict | None = None,
):
    """
    Standard page wrapper with navigation and Factory theme.

    When ``meta`` is provided, emits Open Graph + Twitter Card + canonical URL
    meta tags so blog posts unfurl nicely in Slack, LinkedIn, etc.
    """
    scripts = extra_scripts if extra_scripts else []
    if not isinstance(scripts, list):
        scripts = [scripts]

    meta_tags = []
    if meta:
        og_title = meta.get("title", title)
        og_desc = meta.get("description", "")
        og_image = meta.get("image", "")
        og_url = meta.get("url", "")
        og_type = meta.get("type", "article")
        meta_tags = [
            Meta(property="og:title", content=og_title),
            Meta(property="og:description", content=og_desc),
            Meta(property="og:image", content=og_image),
            Meta(property="og:url", content=og_url),
            Meta(property="og:type", content=og_type),
            Meta(property="og:site_name", content="Gabriel Navarro"),
            Link(rel="canonical", href=og_url) if og_url else None,
            Meta(name="twitter:card", content="summary_large_image"),
            Meta(name="twitter:title", content=og_title),
            Meta(name="twitter:description", content=og_desc),
            Meta(name="twitter:image", content=og_image),
        ]
        meta_tags = [t for t in meta_tags if t is not None]

    return (
        Head(
            Title(title),
            *meta_tags,
            # Geist Font Import
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/sans.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/geist@1.3.0/dist/font/mono.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@fontsource/cascadia-mono@5.2.3/index.min.css",
            ),
        ),
        Style(THEME_CSS + FACTORY_CSS + extra_styles),
        *scripts,
        navigation(),
        Container(
            Section(*content, cls=cls),
            cls="uk-container-large",
        ),
        Footer(),
    )
