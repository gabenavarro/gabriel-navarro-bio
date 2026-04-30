"""Render linted blog markdown to HTML and validate the output.

This module exists so the blog rendering pipeline runs once at submit time
(rather than once per page view), surfaces parser foot-guns when they're
cheap to fix, and stores the final HTML in BigQuery as `body_html`.

See `docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

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


@dataclass
class ValidationIssue:
    """A single issue found by `validate_html`."""

    kind: Literal["p-wraps-svg", "svg-tag-mismatch", "svg-missing-title", "svg-missing-role"]
    line: int | None
    snippet: str


# Tags whose presence inside a <p> wrap is the diagnostic of the class-3 bug.
_SVG_INTERNAL_TAGS = (
    "svg", "text", "rect", "line", "circle", "path",
    "g", "defs", "marker",
)
_P_WRAPS_SVG = re.compile(
    r"<p\b[^>]*>\s*<(?:" + "|".join(_SVG_INTERNAL_TAGS) + r"|!--)\b",
    re.IGNORECASE,
)
_SVG_OPEN = re.compile(r"<svg\b[^>]*>", re.IGNORECASE)
_SVG_CLOSE = re.compile(r"</svg\s*>", re.IGNORECASE)
_SVG_BLOCK = re.compile(r"<svg\b[^>]*>.*?</svg\s*>", re.DOTALL | re.IGNORECASE)
_HAS_ROLE_IMG = re.compile(r'role\s*=\s*"img"', re.IGNORECASE)
_HAS_TITLE_CHILD = re.compile(r"<title\b[^>]*>", re.IGNORECASE)


def _line_of(html: str, offset: int) -> int:
    return html.count("\n", 0, offset) + 1


def validate_html(html: str) -> list[ValidationIssue]:
    """Scan rendered HTML for the four known bad patterns. Returns [] on clean output."""
    issues: list[ValidationIssue] = []

    # Rule 1: <p>-wraps-SVG-internal-tag
    for match in _P_WRAPS_SVG.finditer(html):
        issues.append(ValidationIssue(
            kind="p-wraps-svg",
            line=_line_of(html, match.start()),
            snippet=html[match.start(): match.start() + 120],
        ))

    # Rule 2: <svg> open count == </svg> close count
    n_open = len(_SVG_OPEN.findall(html))
    n_close = len(_SVG_CLOSE.findall(html))
    if n_open != n_close:
        issues.append(ValidationIssue(
            kind="svg-tag-mismatch",
            line=None,
            snippet=f"<svg> opens={n_open}, </svg> closes={n_close}",
        ))

    # Rules 3+4 operate per top-level SVG block.
    # We don't try to detect nesting here — top-level SVGs are the only ones
    # users author; nested SVGs are not used in this project.
    for match in _SVG_BLOCK.finditer(html):
        block = match.group(0)
        line = _line_of(html, match.start())
        if not _HAS_TITLE_CHILD.search(block):
            issues.append(ValidationIssue(
                kind="svg-missing-title",
                line=line,
                snippet=block[:120],
            ))
        # Inspect the opening tag specifically (first match within the block).
        open_match = _SVG_OPEN.match(block)
        if open_match and not _HAS_ROLE_IMG.search(open_match.group(0)):
            issues.append(ValidationIssue(
                kind="svg-missing-role",
                line=line,
                snippet=open_match.group(0),
            ))

    return issues
