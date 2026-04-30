"""Render linted blog markdown to HTML and validate the output.

This module exists so the blog rendering pipeline runs once at submit time
(rather than once per page view), surfaces parser foot-guns when they're
cheap to fix, and stores the final HTML in BigQuery as `body_html`.

See `docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md`.
"""

from __future__ import annotations

from monsterui.all import render_md


class RenderError(Exception):
    """Raised when mistletoe (via monsterui) fails to render a body."""


def render_to_html(body: str) -> str:
    """Render markdown `body` to an HTML string via monsterui.render_md.

    `monsterui.render_md` returns a `NotStr` wrapping HTML; this function
    unwraps it to a plain `str` so callers can store it as a BigQuery
    column or scan it with regex validators.
    """
    try:
        rendered = render_md(body)
    except Exception as exc:  # noqa: BLE001 - we want to wrap any failure
        raise RenderError(f"render_md failed: {exc}") from exc

    # monsterui returns a NotStr (subclass of str). __str__ is the HTML.
    return str(rendered)
