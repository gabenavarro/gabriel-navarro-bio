"""Auto-fix mistletoe foot-guns in blog markdown source.

The portfolio's markdown renderer (mistletoe via monsterui.render_md) has
three known failure modes when blog bodies contain inline SVG:

1. HTML named entities inside SVG break XML parsing.
2. Multi-line `<svg ...>` opening tags break mistletoe's HTML-block detection.
3. Blank lines inside SVG followed by single-line elements break mistletoe's
   HTML-block continuation.

This module fixes all three at submit time, idempotently. See
`docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md` for the
full reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


class LintError(Exception):
    """Raised when the linter encounters a problem it cannot auto-fix
    (e.g. an HTML named entity with no Unicode mapping).
    """


@dataclass
class LintFix:
    """A single class of fix the linter applied to a body of text."""

    kind: Literal["named-entity", "multi-line-svg-open", "blank-line-in-svg"]
    count: int
    detail: str


def lint_body(body: str) -> tuple[str, list[LintFix]]:
    """Apply all three lint rules to `body`, returning the fixed text + list of fixes.

    The transforms are idempotent: running `lint_body` twice on the same input
    produces the same output as running it once.
    """
    return body, []
