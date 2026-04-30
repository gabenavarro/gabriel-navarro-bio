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

import re
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


# Map of HTML named entities to their Unicode literals. The five XML-predefined
# entities (amp/lt/gt/apos/quot) are intentionally absent — they're valid in
# both XML and HTML and do not need substitution.
ENTITY_MAP: dict[str, str] = {
    "mdash": "—", "ndash": "–",
    "middot": "·", "bull": "•",
    "times": "×", "divide": "÷",
    "plusmn": "±", "minus": "−",
    "rarr": "→", "larr": "←",
    "uarr": "↑", "darr": "↓", "harr": "↔",
    "hellip": "…",
    "asymp": "≈", "ne": "≠",
    "ge": "≥", "le": "≤",
    "deg": "°",
    "radic": "√", "infin": "∞",
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ε", "theta": "θ", "lambda": "λ", "mu": "μ",
    "pi": "π", "sigma": "σ", "phi": "φ", "omega": "ω",
    "Sigma": "Σ", "Delta": "Δ", "Omega": "Ω",
    "sum": "∑", "prod": "∏",
    "nbsp": " ",
    "copy": "©", "reg": "®", "trade": "™",
}

_XML_SAFE_ENTITIES = frozenset({"amp", "lt", "gt", "apos", "quot"})
_ENTITY_PATTERN = re.compile(r"&([a-zA-Z][a-zA-Z0-9]*);")


def _replace_named_entities(body: str) -> tuple[str, int]:
    """Replace every HTML named entity with its Unicode literal.

    Returns (transformed_body, count_of_replacements). Raises LintError if
    an entity is encountered that has no mapping in ENTITY_MAP and is not
    one of the five XML-safe entities.
    """
    count = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal count
        name = match.group(1)
        if name in _XML_SAFE_ENTITIES:
            return match.group(0)
        if name in ENTITY_MAP:
            count += 1
            return ENTITY_MAP[name]
        raise LintError(
            f"Unmapped named entity '&{name};'. "
            f"Add a mapping to ENTITY_MAP in src/services/blog_lint.py and re-run."
        )

    return _ENTITY_PATTERN.sub(_sub, body), count


_SVG_OPEN_PATTERN = re.compile(r"<svg\b([^>]*)>", re.DOTALL)


def _collapse_svg_open_tags(body: str) -> tuple[str, int]:
    """Collapse multi-line `<svg ...>` opening tags onto a single line.

    Returns (transformed_body, count_collapsed). A "collapse" means the
    opening tag spanned multiple lines in the source; if it was already on
    one line, no change is recorded for that tag.
    """
    count = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal count
        inner = match.group(1)
        if "\n" not in inner:
            return match.group(0)
        count += 1
        collapsed = re.sub(r"\s+", " ", inner).strip()
        return f"<svg {collapsed}>" if collapsed else "<svg>"

    return _SVG_OPEN_PATTERN.sub(_sub, body), count


_SVG_BLOCK_PATTERN = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL)


def _strip_blank_lines_in_svg(body: str) -> tuple[str, int]:
    """Strip blank lines inside `<svg>...</svg>` blocks.

    Mistletoe terminates HTML blocks at blank lines, which fragments inline
    SVG content. This strips internal blank lines (lines whose only content
    is whitespace) without touching prose blank lines outside SVGs.

    Returns (transformed_body, count_of_blank_lines_stripped).
    """
    total_stripped = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal total_stripped
        block = match.group(0)
        kept = []
        for line in block.split("\n"):
            if line.strip() == "":
                total_stripped += 1
                continue
            kept.append(line)
        return "\n".join(kept)

    return _SVG_BLOCK_PATTERN.sub(_sub, body), total_stripped


_FENCED_CODE_PATTERN = re.compile(r"(^|\n)(```[^\n]*\n.*?\n```)(?=\n|$)", re.DOTALL)


def _stash_fenced_code(body: str) -> tuple[str, list[str]]:
    """Replace each fenced code block with a unique placeholder; return placeholder list.

    The placeholder is a sentinel that won't match any lint regex, so the rest
    of the pipeline ignores code-block content. Caller restores via _restore_fenced_code.
    """
    stash: list[str] = []

    def _sub(match: re.Match[str]) -> str:
        prefix, block = match.group(1), match.group(2)
        idx = len(stash)
        stash.append(block)
        return f"{prefix}__BLOG_LINT_STASH_{idx}__"

    return _FENCED_CODE_PATTERN.sub(_sub, body), stash


def _restore_fenced_code(body: str, stash: list[str]) -> str:
    for idx, block in enumerate(stash):
        body = body.replace(f"__BLOG_LINT_STASH_{idx}__", block)
    return body


def lint_body(body: str) -> tuple[str, list[LintFix]]:
    """Apply all three lint rules to `body`, returning the fixed text + list of fixes.

    The transforms are idempotent: running `lint_body` twice on the same input
    produces the same output as running it once.

    Fenced code blocks (``` ... ```) are stashed before the transforms run and
    restored afterward, so example SVG inside code fences is not mangled by
    the lint rules.
    """
    body, stash = _stash_fenced_code(body)
    fixes: list[LintFix] = []
    body, n = _replace_named_entities(body)
    if n:
        fixes.append(LintFix(
            kind="named-entity",
            count=n,
            detail=f"replaced {n} HTML named entit{'y' if n == 1 else 'ies'} with Unicode literals",
        ))
    body, n = _collapse_svg_open_tags(body)
    if n:
        fixes.append(LintFix(
            kind="multi-line-svg-open",
            count=n,
            detail=f"collapsed {n} multi-line <svg ...> opening tag(s) to single line",
        ))
    body, n = _strip_blank_lines_in_svg(body)
    if n:
        fixes.append(LintFix(
            kind="blank-line-in-svg",
            count=n,
            detail=f"stripped {n} blank line(s) inside <svg>...</svg> blocks",
        ))
    body = _restore_fenced_code(body, stash)
    return body, fixes
