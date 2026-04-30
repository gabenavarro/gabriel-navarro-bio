# Blog HTML Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the blog markdown→HTML render from view time to submit time. Lint mistletoe foot-guns at submit, store rendered HTML as `body_html` in BigQuery, backfill all 22 existing posts, drop the legacy `body` column after a 1-week soak.

**Architecture:** Two new pure-Python modules (`blog_lint.py`, `blog_render.py`) implement auto-fix + render + validate. The CLI's `_payload_from_blog` invokes them in sequence and writes both `body` and `body_html` to BigQuery during the migration window. After backfill + soak, the `body` column and transitional code are removed.

**Tech Stack:** Python 3.13, Pydantic v2, mistletoe (via monsterui.render_md), google-cloud-bigquery, pytest. The `.md` files in `assets/blogs/` remain the source of truth.

**Spec:** `docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md`

---

## File Structure

**New files:**
- `src/services/blog_lint.py` — `LintFix`, `LintError`, `lint_body(body) -> (str, list[LintFix])`. Pure regex transforms; no I/O.
- `src/services/blog_render.py` — `RenderError`, `ValidationIssue`, `render_to_html(body) -> str`, `validate_html(html) -> list[ValidationIssue]`.
- `scripts/__init__.py` — empty.
- `scripts/backfill_blog_html.py` — CLI runner that iterates `assets/blogs/*.md`, runs the new pipeline against each, and updates BigQuery. Has `--dry-run` and a 35-minute streaming-buffer retry.
- `tests/test_blog_lint.py` — bug-class unit tests, idempotency, stash-and-restore, skip-indented-widgets.
- `tests/test_blog_render.py` — render unwrap, validation rule unit tests.
- `tests/test_blog_pipeline_e2e.py` — integration on real posts 0020 (control) + 0022 (canary).
- `tests/test_backfill_blog_html.py` — dry-run mode unit tests; the script's logic in isolation.

**Modified files:**
- `src/services/blog_frontmatter.py` — add `BlogRow` Pydantic model. `BlogFrontmatter` unchanged.
- `src/cli/blog.py` — rewire `_payload_from_blog` (lint→render→validate→BlogRow); upgrade `_cmd_validate` (read-only lint+render+validate).
- `src/models/project.py` — `Project` dataclass adds `body_html: str = ""`. `from_dict` reads it. `body` stays for the transitional period.
- `src/features/projects/projects_page.py:54` — change `render_md(project.body)` to `NotStr(project.body_html)`.

**Final cleanup (after soak):**
- `src/services/blog_frontmatter.py` — drop `body: str` from `BlogRow`.
- `src/cli/blog.py` — adjust `_payload_from_blog` to `exclude={"body"}`.
- `src/models/project.py` — drop `body` field (or keep as optional/deprecated).

**Why this layout:**
- `blog_lint.py` and `blog_render.py` are separate because they have distinct responsibilities (auto-fix source vs render+validate output) and can be tested in isolation. Splitting also keeps each file under 200 lines, which matches the rest of `src/services/`.
- The backfill script lives in `scripts/` (a new sibling of `src/`) because it's a one-shot operational tool, not application code.
- Tests follow the existing one-file-per-module convention in `tests/`.

---

## Phase 1: Foundation — Pure Python (no BigQuery)

### Task 1: Bootstrap `blog_lint.py` module skeleton

**Files:**
- Create: `src/services/blog_lint.py`
- Create: `tests/test_blog_lint.py`

- [ ] **Step 1.1: Write the failing import test**

`tests/test_blog_lint.py`:
```python
"""Tests for src.services.blog_lint."""
import pytest

from src.services.blog_lint import LintError, LintFix, lint_body


def test_module_exports_public_surface():
    """The module exports `LintError`, `LintFix`, `lint_body` as the public API."""
    with pytest.raises(LintError):
        raise LintError("test")
    fix = LintFix(kind="named-entity", count=1, detail="example")
    assert fix.kind == "named-entity"
    assert fix.count == 1
    assert fix.detail == "example"


def test_lint_body_returns_tuple_of_text_and_fixes():
    text = "no svg here, just prose"
    fixed, fixes = lint_body(text)
    assert fixed == text
    assert fixes == []
```

(Both tests in the same file — the first exercises `LintError`/`LintFix` directly so the imports aren't unused, the second locks in the no-op return contract.)

- [ ] **Step 1.2: Run test to verify it fails**

Run: `pytest tests/test_blog_lint.py::test_lint_body_returns_tuple_of_text_and_fixes -v`
Expected: `ImportError` (module doesn't exist yet) or `ModuleNotFoundError`.

- [ ] **Step 1.3: Create the skeleton module**

`src/services/blog_lint.py`:
```python
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
```

- [ ] **Step 1.4: Run test to verify it passes**

Run: `pytest tests/test_blog_lint.py::test_lint_body_returns_tuple_of_text_and_fixes -v`
Expected: PASS.

- [ ] **Step 1.5: Commit**

```bash
git add src/services/blog_lint.py tests/test_blog_lint.py
git commit -m "feat(blog-lint): add module skeleton with LintFix and LintError"
```

---

### Task 2: Implement entity replacement

**Files:**
- Modify: `src/services/blog_lint.py`
- Modify: `tests/test_blog_lint.py`

- [ ] **Step 2.1: Write failing tests**

Append to `tests/test_blog_lint.py`:
```python
import pytest


def test_lint_replaces_mdash_with_unicode():
    src = "<svg><text>A &mdash; B</text></svg>"
    fixed, fixes = lint_body(src)
    assert "&mdash;" not in fixed
    assert "—" in fixed
    assert any(f.kind == "named-entity" and f.count == 1 for f in fixes)


def test_lint_replaces_multiple_named_entities():
    src = "<svg><text>x &times; y &rarr; z</text></svg>"
    fixed, _ = lint_body(src)
    assert "&times;" not in fixed
    assert "&rarr;" not in fixed
    assert "×" in fixed and "→" in fixed


def test_lint_preserves_xml_safe_entities():
    src = "<svg><text>x &lt; y &amp; z &gt; w</text></svg>"
    fixed, fixes = lint_body(src)
    assert fixed == src
    assert fixes == []


def test_lint_raises_on_unmapped_entity():
    src = "<svg><text>nonsense &zzznotreal;</text></svg>"
    with pytest.raises(LintError, match="zzznotreal"):
        lint_body(src)
```

- [ ] **Step 2.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_lint.py -v`
Expected: 3 of the 4 new tests fail (the preserves-xml-safe one passes by accident since the skeleton returns input unchanged).

- [ ] **Step 2.3: Implement `_replace_named_entities`**

In `src/services/blog_lint.py`, add at module level:

```python
import re

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
```

Then update `lint_body` to call it:

```python
def lint_body(body: str) -> tuple[str, list[LintFix]]:
    fixes: list[LintFix] = []
    body, n = _replace_named_entities(body)
    if n:
        fixes.append(LintFix(
            kind="named-entity",
            count=n,
            detail=f"replaced {n} HTML named entit{'y' if n == 1 else 'ies'} with Unicode literals",
        ))
    return body, fixes
```

- [ ] **Step 2.4: Run tests to verify they pass**

Run: `pytest tests/test_blog_lint.py -v`
Expected: all 5 tests PASS.

- [ ] **Step 2.5: Commit**

```bash
git add src/services/blog_lint.py tests/test_blog_lint.py
git commit -m "feat(blog-lint): replace HTML named entities with Unicode literals"
```

---

### Task 3: Collapse multi-line `<svg>` opening tags

**Files:**
- Modify: `src/services/blog_lint.py`
- Modify: `tests/test_blog_lint.py`

- [ ] **Step 3.1: Write failing tests**

Append to `tests/test_blog_lint.py`:
```python
def test_lint_collapses_multi_line_svg_open():
    src = (
        '<svg viewBox="0 0 100 100"\n'
        '     xmlns="http://www.w3.org/2000/svg"\n'
        '     role="img">\n'
        '  <title>x</title>\n'
        '</svg>'
    )
    fixed, fixes = lint_body(src)
    first_line = fixed.split("\n", 1)[0]
    assert first_line == '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img">'
    assert any(f.kind == "multi-line-svg-open" and f.count == 1 for f in fixes)


def test_lint_leaves_single_line_svg_open_alone():
    src = '<svg viewBox="0 0 100 100" xmlns="..." role="img"><title>x</title></svg>'
    fixed, fixes = lint_body(src)
    assert fixed == src
    assert all(f.kind != "multi-line-svg-open" for f in fixes)


def test_lint_collapses_only_svg_tag_not_other_multi_line_tags():
    # <text> spanning lines is FINE — common in SVG body. We only care about <svg> opens.
    src = (
        '<svg viewBox="0 0 100 100" xmlns="..." role="img">\n'
        '  <text x="10" y="20"\n'
        '        font-size="13">hello</text>\n'
        '</svg>'
    )
    fixed, _ = lint_body(src)
    # The multi-line <text> should be unchanged; the <svg> open is already on one line.
    assert "<text x=\"10\" y=\"20\"\n        font-size=\"13\">" in fixed
```

- [ ] **Step 3.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_lint.py -v -k "svg_open or multi_line"`
Expected: 2 of 3 fail (the leaves-single-line one passes vacuously).

- [ ] **Step 3.3: Implement `_collapse_svg_open_tags`**

Add to `src/services/blog_lint.py`:

```python
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
```

Update `lint_body`:

```python
def lint_body(body: str) -> tuple[str, list[LintFix]]:
    fixes: list[LintFix] = []
    body, n = _replace_named_entities(body)
    if n:
        fixes.append(LintFix("named-entity", n, f"replaced {n} HTML named entit{'y' if n == 1 else 'ies'} with Unicode literals"))
    body, n = _collapse_svg_open_tags(body)
    if n:
        fixes.append(LintFix("multi-line-svg-open", n, f"collapsed {n} multi-line <svg ...> opening tag(s) to single line"))
    return body, fixes
```

- [ ] **Step 3.4: Run tests**

Run: `pytest tests/test_blog_lint.py -v`
Expected: all PASS.

- [ ] **Step 3.5: Commit**

```bash
git add src/services/blog_lint.py tests/test_blog_lint.py
git commit -m "feat(blog-lint): collapse multi-line <svg> opening tags to single line"
```

---

### Task 4: Strip blank lines inside SVG blocks

**Files:**
- Modify: `src/services/blog_lint.py`
- Modify: `tests/test_blog_lint.py`

- [ ] **Step 4.1: Write failing tests**

Append to `tests/test_blog_lint.py`:
```python
def test_lint_strips_blank_lines_inside_svg():
    src = (
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>line a</text>\n'
        '\n'
        '  <text>line b</text>\n'
        '</svg>'
    )
    fixed, fixes = lint_body(src)
    inside = fixed[fixed.index("<svg>"):fixed.index("</svg>")]
    assert "\n\n" not in inside
    assert "<text>line a</text>" in fixed and "<text>line b</text>" in fixed
    assert any(f.kind == "blank-line-in-svg" for f in fixes)


def test_lint_preserves_blank_lines_outside_svg():
    src = (
        "Paragraph one.\n"
        "\n"
        "Paragraph two.\n"
        "\n"
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>x</text>\n'
        '</svg>\n'
        "\n"
        "Paragraph three.\n"
    )
    fixed, _ = lint_body(src)
    assert "Paragraph one.\n\nParagraph two." in fixed
    assert "</svg>\n\nParagraph three." in fixed


def test_lint_preserves_indentation_in_svg():
    src = (
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>indented body</text>\n'
        '</svg>'
    )
    fixed, _ = lint_body(src)
    assert "  <text>indented body</text>" in fixed
```

- [ ] **Step 4.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_lint.py -v -k "blank_line or outside_svg or indentation"`
Expected: at least 2 fail.

- [ ] **Step 4.3: Implement `_strip_blank_lines_in_svg`**

Add to `src/services/blog_lint.py`:

```python
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
```

Update `lint_body`:

```python
def lint_body(body: str) -> tuple[str, list[LintFix]]:
    fixes: list[LintFix] = []
    body, n = _replace_named_entities(body)
    if n:
        fixes.append(LintFix("named-entity", n, f"replaced {n} HTML named entit{'y' if n == 1 else 'ies'} with Unicode literals"))
    body, n = _collapse_svg_open_tags(body)
    if n:
        fixes.append(LintFix("multi-line-svg-open", n, f"collapsed {n} multi-line <svg ...> opening tag(s) to single line"))
    body, n = _strip_blank_lines_in_svg(body)
    if n:
        fixes.append(LintFix("blank-line-in-svg", n, f"stripped {n} blank line(s) inside <svg>...</svg> blocks"))
    return body, fixes
```

- [ ] **Step 4.4: Run tests**

Run: `pytest tests/test_blog_lint.py -v`
Expected: all PASS.

- [ ] **Step 4.5: Commit**

```bash
git add src/services/blog_lint.py tests/test_blog_lint.py
git commit -m "feat(blog-lint): strip blank lines inside <svg> blocks"
```

---

### Task 5: Stash and restore fenced code blocks

**Files:**
- Modify: `src/services/blog_lint.py`
- Modify: `tests/test_blog_lint.py`

**Why:** The skill's `references/svg_diagrams.md` (and any tutorial post about SVG) contains fenced code blocks like ` ```svg\n<svg ...>\n``` ` that demonstrate SVG syntax. The lint rules above would mangle the example — collapsing multi-line opens, stripping internal blanks. We need to preserve fenced code verbatim. The cleanest pattern is **stash** all fenced code blocks before lint, run the rules on the rest, **restore** the stashed blocks.

- [ ] **Step 5.1: Write failing test**

Append to `tests/test_blog_lint.py`:
```python
def test_lint_does_not_mangle_fenced_code_blocks():
    src = (
        "Here's the template:\n"
        "\n"
        "```svg\n"
        '<svg viewBox="0 0 100 100"\n'
        '     xmlns="..."\n'
        '     role="img">\n'
        "\n"
        "  <text>example</text>\n"
        "</svg>\n"
        "```\n"
        "\n"
        "And here's a real one:\n"
        "\n"
        '<svg viewBox="0 0 200 200" xmlns="..." role="img">\n'
        '  <title>real</title>\n'
        "\n"
        "  <text>real text</text>\n"
        "</svg>\n"
    )
    fixed, fixes = lint_body(src)
    # The CODE BLOCK content must be preserved verbatim — multi-line open and blanks stay.
    assert (
        '```svg\n'
        '<svg viewBox="0 0 100 100"\n'
        '     xmlns="..."\n'
        '     role="img">\n'
        "\n"
        "  <text>example</text>\n"
        "</svg>\n"
        "```"
    ) in fixed
    # The REAL <svg> outside the code block IS linted (no internal blank line).
    real_block_start = fixed.index('<svg viewBox="0 0 200 200"')
    real_block_end = fixed.index("</svg>", real_block_start)
    real_block = fixed[real_block_start:real_block_end]
    assert "\n\n" not in real_block
```

- [ ] **Step 5.2: Run test to verify it fails**

Run: `pytest tests/test_blog_lint.py::test_lint_does_not_mangle_fenced_code_blocks -v`
Expected: FAIL (the lint mangles the code block).

- [ ] **Step 5.3: Implement stash/restore around lint_body**

Add at the top of the lint pipeline (above `_replace_named_entities` etc., or refactor `lint_body`):

```python
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
```

Update `lint_body`:

```python
def lint_body(body: str) -> tuple[str, list[LintFix]]:
    body, stash = _stash_fenced_code(body)
    fixes: list[LintFix] = []
    body, n = _replace_named_entities(body)
    if n:
        fixes.append(LintFix("named-entity", n, f"replaced {n} HTML named entit{'y' if n == 1 else 'ies'} with Unicode literals"))
    body, n = _collapse_svg_open_tags(body)
    if n:
        fixes.append(LintFix("multi-line-svg-open", n, f"collapsed {n} multi-line <svg ...> opening tag(s) to single line"))
    body, n = _strip_blank_lines_in_svg(body)
    if n:
        fixes.append(LintFix("blank-line-in-svg", n, f"stripped {n} blank line(s) inside <svg>...</svg> blocks"))
    body = _restore_fenced_code(body, stash)
    return body, fixes
```

- [ ] **Step 5.4: Run all blog_lint tests**

Run: `pytest tests/test_blog_lint.py -v`
Expected: all PASS, including the new code-block test.

- [ ] **Step 5.5: Commit**

```bash
git add src/services/blog_lint.py tests/test_blog_lint.py
git commit -m "feat(blog-lint): stash fenced code blocks before lint to preserve examples"
```

---

### Task 6: Idempotency, indented widget SVGs, regression on real fixture

**Files:**
- Modify: `tests/test_blog_lint.py`

- [ ] **Step 6.1: Write three more tests**

Append to `tests/test_blog_lint.py`:
```python
def test_lint_is_idempotent():
    """Running lint twice on the same input produces the same output as once."""
    src = (
        '<svg viewBox="0 0 100 100"\n'
        '     xmlns="..."\n'
        '     role="img">\n'
        '  <title>t &mdash; subtitle</title>\n'
        '\n'
        '  <text>x &times; y</text>\n'
        '</svg>'
    )
    once, _ = lint_body(src)
    twice, fixes_second = lint_body(once)
    assert once == twice
    assert fixes_second == []  # second pass is a no-op


def test_lint_does_not_mangle_indented_widget_svg():
    """SVG indented as a child of <div class="ptb-state"> is left alone by the
    blank-line rule; the surrounding <div> already prevents mistletoe from
    breaking the SVG, so the lint shouldn't touch the indentation.

    The strip_blank_lines_in_svg rule operates inside <svg>...</svg> regardless
    of indentation, which is fine because indented SVGs typically don't have
    blank lines inside in the first place. This test guards against any future
    rule that might be too aggressive about indentation.
    """
    src = (
        '<div class="ptb-state" id="s1">\n'
        '    <svg viewBox="0 0 100 100" xmlns="..." role="img">\n'
        '      <title>indented</title>\n'
        '      <text>x</text>\n'
        '    </svg>\n'
        '</div>'
    )
    fixed, fixes = lint_body(src)
    # No changes expected — this SVG is already lint-clean.
    assert fixed == src
    assert fixes == []


def test_lint_canary_against_real_post_0022():
    """Regression guard: lint reduces 0022 to a state with no internal SVG blanks.

    This is the post that originally exhibited all three bug classes. We don't
    assert byte-equality (that would be brittle if the post is edited); we
    assert that after lint, the body has no <svg> block with a blank line in it.
    """
    from pathlib import Path
    src = Path("assets/blogs/0022-spike-sparse-sink-anatomy-massive.md").read_text(encoding="utf-8")
    fixed, _ = lint_body(src)
    # Find every <svg>...</svg> and check no blank line inside.
    import re
    for m in re.finditer(r"<svg\b[^>]*>.*?</svg>", fixed, re.DOTALL):
        block = m.group(0)
        for line in block.split("\n"):
            assert line.strip() != "", f"Blank line found inside SVG block: {block[:120]!r}..."
```

- [ ] **Step 6.2: Run tests**

Run: `pytest tests/test_blog_lint.py -v`
Expected: all PASS. (The canary test will pass because the user already pushed the lint fix for 0022 in an earlier session — but it serves as a regression guard against future drift.)

- [ ] **Step 6.3: Commit**

```bash
git add tests/test_blog_lint.py
git commit -m "test(blog-lint): idempotency, indented widget skip, real-post canary"
```

---

### Task 7: `blog_render.py` — render_to_html

**Files:**
- Create: `src/services/blog_render.py`
- Create: `tests/test_blog_render.py`

- [ ] **Step 7.1: Write failing test**

`tests/test_blog_render.py`:
```python
"""Tests for src.services.blog_render."""
import pytest
from src.services.blog_render import RenderError, render_to_html


def test_render_passes_simple_markdown_to_html():
    md = "# Hello\n\nWorld."
    html = render_to_html(md)
    assert "<h1" in html  # monsterui adds classes; just check the tag opened
    assert "Hello" in html
    assert "<p" in html
    assert "World." in html


def test_render_returns_plain_string_not_notstr():
    """The function must return `str`, not a FastHTML NotStr/FT object."""
    html = render_to_html("plain")
    assert isinstance(html, str)


def test_render_preserves_inline_svg_when_clean():
    md = (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img">\n'
        '  <title>t</title>\n'
        '  <text>x</text>\n'
        '</svg>'
    )
    html = render_to_html(md)
    assert "<svg" in html
    assert "<title" in html  # monsterui may rewrite case but tag stays
    assert "<text" in html
    # The diagnostic for the bug we're fixing — must NOT appear:
    assert "<p><svg" not in html
    assert "<p><text" not in html
```

- [ ] **Step 7.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_render.py -v`
Expected: ImportError.

- [ ] **Step 7.3: Implement `render_to_html`**

`src/services/blog_render.py`:
```python
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
```

- [ ] **Step 7.4: Run tests**

Run: `pytest tests/test_blog_render.py -v`
Expected: all PASS.

- [ ] **Step 7.5: Commit**

```bash
git add src/services/blog_render.py tests/test_blog_render.py
git commit -m "feat(blog-render): render markdown to HTML via monsterui.render_md"
```

---

### Task 8: `blog_render.py` — validate_html with four rules

**Files:**
- Modify: `src/services/blog_render.py`
- Modify: `tests/test_blog_render.py`

- [ ] **Step 8.1: Write failing tests**

Append to `tests/test_blog_render.py`:
```python
from src.services.blog_render import ValidationIssue, validate_html


def test_validate_returns_empty_for_clean_html():
    html = '<svg viewBox="0 0 1 1" role="img"><title>t</title></svg>'
    assert validate_html(html) == []


def test_validate_catches_p_wrapping_svg():
    bad = '<p><svg></svg></p>'
    issues = validate_html(bad)
    assert any(i.kind == "p-wraps-svg" for i in issues)


def test_validate_catches_p_wrapping_text():
    bad = '<svg role="img"><title>t</title></svg>\n<p><text x="0">stray</text></p>'
    issues = validate_html(bad)
    assert any(i.kind == "p-wraps-svg" for i in issues)


def test_validate_catches_svg_tag_mismatch():
    bad = '<svg role="img"><title>t</title>'  # missing </svg>
    issues = validate_html(bad)
    assert any(i.kind == "svg-tag-mismatch" for i in issues)


def test_validate_catches_svg_missing_title():
    bad = '<svg viewBox="0 0 1 1" role="img"><text>x</text></svg>'  # no <title>
    issues = validate_html(bad)
    assert any(i.kind == "svg-missing-title" for i in issues)


def test_validate_catches_svg_missing_role_img():
    bad = '<svg viewBox="0 0 1 1"><title>t</title></svg>'  # no role="img"
    issues = validate_html(bad)
    assert any(i.kind == "svg-missing-role" for i in issues)


def test_validate_returns_multiple_issues_at_once():
    bad = '<p><svg></svg></p><p><text>x</text></p>'  # two <p> wraps + tag mismatch + missing title
    issues = validate_html(bad)
    kinds = [i.kind for i in issues]
    assert kinds.count("p-wraps-svg") >= 2


def test_validate_issue_includes_snippet():
    bad = '<p><svg></svg></p>'
    issues = validate_html(bad)
    p_issues = [i for i in issues if i.kind == "p-wraps-svg"]
    assert len(p_issues) >= 1
    assert "<svg" in p_issues[0].snippet
```

- [ ] **Step 8.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_render.py -v`
Expected: ImportError on `ValidationIssue` and `validate_html`.

- [ ] **Step 8.3: Implement `validate_html`**

Append to `src/services/blog_render.py`:

```python
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
```

- [ ] **Step 8.4: Run tests**

Run: `pytest tests/test_blog_render.py -v`
Expected: all PASS.

- [ ] **Step 8.5: Commit**

```bash
git add src/services/blog_render.py tests/test_blog_render.py
git commit -m "feat(blog-render): validate_html with four bad-pattern rules"
```

---

## Phase 2: Pydantic + CLI wiring

### Task 9: Add `BlogRow` Pydantic model

**Files:**
- Modify: `src/services/blog_frontmatter.py`
- Modify: `tests/test_blog_frontmatter.py`

- [ ] **Step 9.1: Write failing tests**

Append to `tests/test_blog_frontmatter.py`:
```python
def test_blog_row_validates_minimal_payload():
    """BlogRow accepts a complete payload (markdown + html) with no errors."""
    from datetime import datetime, timezone
    from src.services.blog_frontmatter import BlogRow
    row = BlogRow(
        id="00000000-0000-0000-0000-000000000000",
        title="Test",
        date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        tags=["test"],
        description="d",
        image="https://example.com/img.svg",
        type="note",
        disabled=False,
        views=0,
        likes=0,
        body="# md",
        body_html="<h1>md</h1>",
    )
    assert row.body_html == "<h1>md</h1>"


def test_blog_row_rejects_empty_body_html():
    from datetime import datetime, timezone
    from pydantic import ValidationError
    from src.services.blog_frontmatter import BlogRow
    with pytest.raises(ValidationError, match="body_html"):
        BlogRow(
            id="x",
            title="t",
            date=datetime(2026, 1, 1, tzinfo=timezone.utc),
            tags=[],
            description="d",
            image="https://e.com/i.svg",
            type="note",
            disabled=False,
            views=0,
            likes=0,
            body="md",
            body_html="   ",  # whitespace only — invalid
        )


def test_blog_row_extra_fields_forbidden():
    from datetime import datetime, timezone
    from pydantic import ValidationError
    from src.services.blog_frontmatter import BlogRow
    with pytest.raises(ValidationError):
        BlogRow(
            id="x", title="t",
            date=datetime(2026, 1, 1, tzinfo=timezone.utc),
            tags=[], description="d",
            image="https://e.com/i.svg",
            type="note", disabled=False, views=0, likes=0,
            body="md", body_html="<h1/>",
            unexpected="boom",
        )
```

- [ ] **Step 9.2: Run tests to verify they fail**

Run: `pytest tests/test_blog_frontmatter.py -v -k blog_row`
Expected: ImportError on `BlogRow`.

- [ ] **Step 9.3: Add `BlogRow` to `src/services/blog_frontmatter.py`**

Append to `src/services/blog_frontmatter.py`:

```python
class BlogRow(BaseModel):
    """The shape of a row in the BigQuery `gn-blog` table.

    During the migration window this carries both `body` (legacy markdown)
    and `body_html` (rendered HTML). After the legacy `body` column is
    dropped from the BigQuery table, `body` will be removed from this model
    and `_payload_from_blog` in src.cli.blog will stop populating it.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    date: datetime
    tags: list[str]
    description: str
    image: HttpUrl
    type: Literal["note", "article"]
    disabled: bool
    views: int
    likes: int
    body: str
    body_html: str

    @field_validator("body_html")
    @classmethod
    def _body_html_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("body_html must be non-empty")
        return value
```

- [ ] **Step 9.4: Run tests**

Run: `pytest tests/test_blog_frontmatter.py -v`
Expected: all PASS, including the new BlogRow tests AND every pre-existing test (the existing `BlogFrontmatter` is untouched).

- [ ] **Step 9.5: Commit**

```bash
git add src/services/blog_frontmatter.py tests/test_blog_frontmatter.py
git commit -m "feat(blog-frontmatter): add BlogRow Pydantic model for BigQuery payload"
```

---

### Task 10: Wire `_payload_from_blog` to lint+render+validate

**Files:**
- Modify: `src/cli/blog.py`
- Modify: `tests/test_cli_blog.py`

- [ ] **Step 10.1: Write failing tests**

Append to `tests/test_cli_blog.py`:
```python
def test_payload_from_blog_includes_body_html(tmp_path):
    """_payload_from_blog returns a dict with both `body` (markdown) and
    `body_html` (rendered)."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    md.write_text(
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n",
        encoding="utf-8",
    )
    payload = _payload_from_blog(md)
    assert "body" in payload
    assert "body_html" in payload
    assert "<h1" in payload["body_html"]


def test_payload_from_blog_persists_lint_fixes_to_disk(tmp_path, capsys):
    """If lint changes the body, the .md file is overwritten with the linted text."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    raw = (
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n"
        '<svg viewBox="0 0 100 100" xmlns="..." role="img">\n'
        "  <title>x &mdash; y</title>\n"
        "  <text>z</text>\n"
        "</svg>\n"
    )
    md.write_text(raw, encoding="utf-8")
    _payload_from_blog(md)
    after = md.read_text(encoding="utf-8")
    assert "&mdash;" not in after
    assert "—" in after
    captured = capsys.readouterr()
    assert "[lint]" in captured.out


def test_payload_from_blog_raises_on_validation_failure(tmp_path):
    """If validate_html finds an issue, _payload_from_blog raises."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    # Body contains an SVG with no <title> and no role="img" — both will fail validation.
    md.write_text(
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n"
        "<svg viewBox=\"0 0 100 100\"><text>x</text></svg>\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="validate_html"):
        _payload_from_blog(md)
```

(Add `import pytest` at the top of the file if it's not already there.)

- [ ] **Step 10.2: Run tests to verify they fail**

Run: `pytest tests/test_cli_blog.py -v -k payload_from_blog`
Expected: 3 fails (current `_payload_from_blog` doesn't lint, render, or write back).

- [ ] **Step 10.3: Rewire `_payload_from_blog`**

In `src/cli/blog.py`:

1. Update imports:
```python
from src.services.blog_frontmatter import BlogRow, ensure_id, parse_blog
from src.services.blog_lint import LintError, lint_body
from src.services.blog_render import RenderError, render_to_html, validate_html
```

2. Replace the body of `_payload_from_blog` with:
```python
def _payload_from_blog(path: Path) -> dict[str, Any]:
    """Parse `path`, lint the body, render to HTML, validate, and return a BlogRow dict.

    Side effects:
      * Backfills a UUID into the file (via ensure_id) if missing.
      * Writes lint fixes back to the file if any rule applied.
    """
    ensure_id(path)
    blog = parse_blog(path)

    try:
        fixed_body, fixes = lint_body(blog.body)
    except LintError as exc:
        raise ValueError(f"lint_body failed: {exc}") from exc

    if fixes and fixed_body != blog.body:
        _persist_body_to_file(path, blog.body, fixed_body)
        for f in fixes:
            print(f"[lint] {f.kind}: {f.detail}")
        # Re-parse so the in-memory model reflects the on-disk file.
        blog = parse_blog(path)

    try:
        html = render_to_html(blog.body)
    except RenderError as exc:
        raise ValueError(f"render_to_html failed: {exc}") from exc

    issues = validate_html(html)
    if issues:
        for i in issues:
            print(
                f"[error] {i.kind} (line {i.line}): {i.snippet[:120]}",
                file=sys.stderr,
            )
        raise ValueError(
            f"validate_html found {len(issues)} issue(s); fix the source and re-run"
        )

    row = BlogRow(**{**blog.model_dump(), "body_html": html})
    return row.model_dump(mode="json")


def _persist_body_to_file(path: Path, old_body: str, new_body: str) -> None:
    """Replace the body of `path` with `new_body`, preserving the frontmatter block.

    Writes byte-for-byte except for the body section after the closing
    frontmatter delimiter.
    """
    text = path.read_text(encoding="utf-8")
    if not text.endswith(old_body):
        # Defensive: the body should always be the trailing portion of the file.
        # If it's not, refuse to mangle the file.
        raise ValueError(
            f"refusing to persist lint fixes: body of {path} does not appear at end of file"
        )
    new_text = text[: -len(old_body)] + new_body
    path.write_text(new_text, encoding="utf-8")
```

- [ ] **Step 10.4: Run all CLI tests**

Run: `pytest tests/test_cli_blog.py -v`
Expected: all PASS, including new tests AND existing validate-only ones.

- [ ] **Step 10.5: Commit**

```bash
git add src/cli/blog.py tests/test_cli_blog.py
git commit -m "feat(cli-blog): wire _payload_from_blog to lint+render+validate"
```

---

### Task 11: Upgrade `_cmd_validate` to read-only lint+render+validate

**Files:**
- Modify: `src/cli/blog.py`
- Modify: `tests/test_cli_blog.py`

- [ ] **Step 11.1: Write failing tests**

Append to `tests/test_cli_blog.py`:
```python
def test_validate_reports_lint_issues_without_writing(tmp_path, capsys):
    """`blog validate` reports lint issues but does NOT write the file."""
    from src.cli.__main__ import main
    md = tmp_path / "post.md"
    raw = (
        "@{id = \"00000000-0000-0000-0000-000000000000\"\n"
        "  title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# B\n<svg viewBox=\"0 0 1 1\" xmlns=\"...\" role=\"img\"><title>x &mdash; y</title></svg>\n"
    )
    md.write_text(raw, encoding="utf-8")
    rc = main(["blog", "validate", str(md)])
    assert rc == 0
    after = md.read_text(encoding="utf-8")
    # File must be unchanged.
    assert after == raw
    captured = capsys.readouterr()
    # Validate should report what lint WOULD do.
    assert "lint" in captured.out.lower() or "would" in captured.out.lower()


def test_validate_exits_nonzero_on_validation_issue(tmp_path):
    """`blog validate` exits nonzero when validate_html finds an issue."""
    from src.cli.__main__ import main
    md = tmp_path / "post.md"
    md.write_text(
        "@{id = \"00000000-0000-0000-0000-000000000000\"\n"
        "  title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# B\n<svg viewBox=\"0 0 1 1\"><text>missing title and role</text></svg>\n",
        encoding="utf-8",
    )
    rc = main(["blog", "validate", str(md)])
    assert rc == 1
```

- [ ] **Step 11.2: Run tests to verify they fail**

Run: `pytest tests/test_cli_blog.py -v -k "lint_issues_without_writing or validation_issue"`
Expected: 2 fails.

- [ ] **Step 11.3: Implement read-only `_cmd_validate`**

Replace `_cmd_validate` in `src/cli/blog.py`:

```python
def _cmd_validate(args: argparse.Namespace) -> int:
    """Read-only check: parse, run lint preview, render, validate.

    Does NOT write to disk and does NOT submit to BigQuery. Use this from
    pre-commit or CI to catch issues before `submit`.
    """
    try:
        blog = parse_blog(args.path)
    except Exception as exc:  # noqa: BLE001
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    # Lint preview — report what `submit` would auto-fix, but don't write.
    try:
        _, fixes = lint_body(blog.body)
    except LintError as exc:
        print(f"INVALID (lint): {exc}", file=sys.stderr)
        return 1
    for f in fixes:
        print(f"[lint preview] would {f.kind}: {f.detail}")

    # Render + validate against the LINTED body, since that's what submit would push.
    fixed_body, _ = lint_body(blog.body)
    try:
        html = render_to_html(fixed_body)
    except RenderError as exc:
        print(f"INVALID (render): {exc}", file=sys.stderr)
        return 1

    issues = validate_html(html)
    if issues:
        for i in issues:
            print(f"[error] {i.kind} (line {i.line}): {i.snippet[:120]}", file=sys.stderr)
        return 1

    print(f"OK: {blog.title}")
    return 0
```

- [ ] **Step 11.4: Run all CLI tests**

Run: `pytest tests/test_cli_blog.py -v`
Expected: all PASS, including pre-existing tests like `test_blog_validate_exits_zero_on_valid_file`.

- [ ] **Step 11.5: Commit**

```bash
git add src/cli/blog.py tests/test_cli_blog.py
git commit -m "feat(cli-blog): upgrade validate command to read-only lint+render+validate"
```

---

## Phase 3: End-to-end pipeline tests

### Task 12: E2E tests against real posts 0020 and 0022

**Files:**
- Create: `tests/test_blog_pipeline_e2e.py`

- [ ] **Step 12.1: Write the E2E suite**

`tests/test_blog_pipeline_e2e.py`:
```python
"""End-to-end tests: real posts through the full pipeline (lint → render → validate).

Uses real files in assets/blogs/ as fixtures. These tests run BEFORE BigQuery
is touched — they exercise pure-Python pipeline only.
"""
from pathlib import Path

from src.services.blog_lint import lint_body
from src.services.blog_render import render_to_html, validate_html


def _full_pipeline(md_path: Path) -> tuple[str, list]:
    """Run a markdown file through lint → render → validate.

    Returns (rendered_html, validation_issues). Does not write to disk.
    """
    src = md_path.read_text(encoding="utf-8")
    fixed, _ = lint_body(src)
    html = render_to_html(fixed)
    return html, validate_html(html)


def test_e2e_post_0020_renders_clean():
    """Control: a prose-heavy post with a few SVGs renders with no issues."""
    html, issues = _full_pipeline(Path("assets/blogs/0020-fm-purturb.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"
    assert len(html) > 1000  # sanity: didn't render to nothing


def test_e2e_post_0022_renders_clean():
    """Canary: post 0022 originally had 33 mistletoe foot-gun sites; must be clean now."""
    html, issues = _full_pipeline(Path("assets/blogs/0022-spike-sparse-sink-anatomy-massive.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"
    # Spot-check that the SVGs survived.
    assert html.count("<svg") >= 10


def test_e2e_post_0001_renders_clean():
    """Old prose-only post (no SVG) should still pass through cleanly."""
    html, issues = _full_pipeline(Path("assets/blogs/0001-fastp.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"


def test_e2e_lint_is_idempotent_against_real_posts():
    """Running lint twice on every real post produces identical output."""
    for md_path in sorted(Path("assets/blogs").glob("*.md")):
        src = md_path.read_text(encoding="utf-8")
        once, _ = lint_body(src)
        twice, _ = lint_body(once)
        assert once == twice, f"lint is not idempotent on {md_path.name}"
```

- [ ] **Step 12.2: Run the suite**

Run: `pytest tests/test_blog_pipeline_e2e.py -v`
Expected: all PASS. If a real post fails, that's signal — investigate, do not silence.

- [ ] **Step 12.3: Commit**

```bash
git add tests/test_blog_pipeline_e2e.py
git commit -m "test(blog-pipeline): e2e on real posts 0001/0020/0022 + idempotency sweep"
```

---

## Phase 4: BigQuery schema + backfill

### Task 13: Add `body_html` column

**Files:** none (BigQuery DDL)

- [ ] **Step 13.1: Run the DDL**

```bash
bq query --nouse_legacy_sql \
  'ALTER TABLE `noble-office-299208.portfolio.gn-blog` ADD COLUMN body_html STRING;'
```

- [ ] **Step 13.2: Verify the column exists**

```bash
bq show --schema --format=prettyjson noble-office-299208:portfolio.gn-blog | grep -c '"name": "body_html"'
```
Expected: `1`.

- [ ] **Step 13.3: Smoke-test a single submit**

Pick one post (e.g. 0021-portello.md) and run:
```bash
python -m src.cli blog submit assets/blogs/0021-portello.md --dry-run
```
Expected: prints `[dry-run] would insert into noble-office-299208.portfolio.gn-blog:` followed by JSON containing both `"body": "..."` and `"body_html": "<...>"`.

If submit works against a freshly added column without errors, the schema migration is healthy.

- [ ] **Step 13.4: Document the DDL ran**

Append to `docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md` under "Schema migration":

```markdown
**Migration log:**
- YYYY-MM-DD HH:MM UTC — `ALTER TABLE ... ADD COLUMN body_html STRING;` executed; verified via `bq show`.
```

```bash
git add docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md
git commit -m "chore(bq): add body_html column to gn-blog table"
```

---

### Task 14: `scripts/backfill_blog_html.py` — dry-run mode

**Files:**
- Create: `scripts/__init__.py` (empty)
- Create: `scripts/backfill_blog_html.py`
- Create: `tests/test_backfill_blog_html.py`

- [ ] **Step 14.1: Write failing tests for the dry-run logic**

`tests/test_backfill_blog_html.py`:
```python
"""Tests for scripts.backfill_blog_html."""
from pathlib import Path

import pytest


def test_iter_blog_paths_returns_sorted_md_files(tmp_path):
    from scripts.backfill_blog_html import iter_blog_paths
    (tmp_path / "0003-c.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "0001-a.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "0002-b.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "skip.txt").write_text("not md", encoding="utf-8")

    paths = iter_blog_paths(tmp_path)
    names = [p.name for p in paths]
    assert names == ["0001-a.md", "0002-b.md", "0003-c.md"]


def test_dry_run_does_not_call_submit(tmp_path, monkeypatch, capsys):
    """In --dry-run mode, the script previews each file without invoking BigQuery."""
    from scripts.backfill_blog_html import run_backfill
    from src.cli import blog as blog_module

    submit_calls: list[str] = []
    monkeypatch.setattr(
        blog_module, "_cmd_submit", lambda args: submit_calls.append(str(args.path)) or 0
    )

    # Stub out _payload_from_blog so we don't need real Pydantic frontmatter.
    def fake_payload(path):
        return {"id": "x", "body": path.read_text(), "body_html": "<p>html</p>"}
    monkeypatch.setattr(blog_module, "_payload_from_blog", fake_payload)

    blogs = tmp_path / "blogs"
    blogs.mkdir()
    (blogs / "0001-a.md").write_text("@{}\nbody", encoding="utf-8")

    rc = run_backfill(blogs, dry_run=True)
    assert rc == 0
    assert submit_calls == []  # nothing pushed
    captured = capsys.readouterr()
    assert "0001-a.md" in captured.out


def test_classify_streaming_buffer_error_recognizes_known_message():
    from scripts.backfill_blog_html import is_streaming_buffer_error

    class MockExc(Exception):
        pass

    err = MockExc("UPDATE or DELETE statement over table ... would affect rows in the streaming buffer, which is not supported")
    assert is_streaming_buffer_error(err)
    assert not is_streaming_buffer_error(MockExc("permission denied"))
```

- [ ] **Step 14.2: Run tests to verify they fail**

Run: `pytest tests/test_backfill_blog_html.py -v`
Expected: ImportError on `scripts.backfill_blog_html`.

- [ ] **Step 14.3: Create the script**

`scripts/__init__.py`:
```python
"""Operational scripts (one-shots / migrations)."""
```

`scripts/backfill_blog_html.py`:
```python
"""Backfill body_html for every blog post in /app/assets/blogs.

Usage:
    python scripts/backfill_blog_html.py --dry-run   # preview only
    python scripts/backfill_blog_html.py             # execute (one update per post)

In execute mode, each post is processed:
  1. Run _payload_from_blog (lint → render → validate) and persist any lint fixes
     to the .md file.
  2. If --dry-run, print a one-line summary and continue.
  3. Otherwise call `python -m src.cli blog update <path>` (DELETE + INSERT).

BigQuery's streaming buffer rejects DML on rows inserted within the last
~30 minutes. The script collects streaming-buffer failures, sleeps 35 min,
and retries them once. Anything that still fails after retry is reported
and the script exits non-zero.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BLOGS_DIR = REPO_ROOT / "assets" / "blogs"
STREAMING_BUFFER_MARKER = "streaming buffer"


def iter_blog_paths(blogs_dir: Path) -> list[Path]:
    """Return all `*.md` files in `blogs_dir`, sorted by filename."""
    return sorted(p for p in blogs_dir.iterdir() if p.suffix == ".md" and p.is_file())


def is_streaming_buffer_error(exc: BaseException) -> bool:
    """Heuristic: BigQuery surfaces this exact phrase in the error message."""
    return STREAMING_BUFFER_MARKER in str(exc).lower()


def run_backfill(blogs_dir: Path, dry_run: bool) -> int:
    """Iterate blogs and submit updates. Return 0 on success, 1 on failures."""
    from argparse import Namespace
    from src.cli import blog as blog_module

    paths = iter_blog_paths(blogs_dir)
    print(f"Found {len(paths)} blog post(s) in {blogs_dir}.")

    successes: list[Path] = []
    streaming_failures: list[Path] = []
    hard_failures: list[tuple[Path, str]] = []

    for path in paths:
        print(f"\n--- {path.name} ---")
        try:
            payload = blog_module._payload_from_blog(path)
        except Exception as exc:  # noqa: BLE001
            hard_failures.append((path, f"payload error: {exc}"))
            continue

        if dry_run:
            print(f"[dry-run] would update id={payload.get('id', '?')} (body_html: {len(payload.get('body_html', ''))} chars)")
            successes.append(path)
            continue

        ns = Namespace(path=path, dry_run=False, table=None)
        try:
            rc = blog_module._cmd_update(ns)
        except Exception as exc:
            if is_streaming_buffer_error(exc):
                print(f"[stream-buffer] {path.name} hit streaming-buffer; will retry")
                streaming_failures.append(path)
                continue
            hard_failures.append((path, f"update raised: {exc}"))
            continue
        if rc != 0:
            hard_failures.append((path, f"update returned {rc}"))
        else:
            successes.append(path)

    if streaming_failures and not dry_run:
        print(f"\n=== Sleeping 35 minutes before retrying {len(streaming_failures)} streaming-buffer post(s) ===")
        time.sleep(35 * 60)
        for path in streaming_failures:
            print(f"\n--- retry: {path.name} ---")
            ns = Namespace(path=path, dry_run=False, table=None)
            try:
                rc = blog_module._cmd_update(ns)
            except Exception as exc:
                hard_failures.append((path, f"retry raised: {exc}"))
                continue
            if rc != 0:
                hard_failures.append((path, f"retry returned {rc}"))
            else:
                successes.append(path)

    print("\n=== Summary ===")
    print(f"  succeeded: {len(successes)}")
    print(f"  hard-failed: {len(hard_failures)}")
    for p, reason in hard_failures:
        print(f"    - {p.name}: {reason}")
    return 0 if not hard_failures else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview only; do not push to BigQuery.")
    parser.add_argument("--blogs-dir", default=str(DEFAULT_BLOGS_DIR), help="Directory containing the blog .md files.")
    args = parser.parse_args(argv)
    return run_backfill(Path(args.blogs_dir), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 14.4: Run tests**

Run: `pytest tests/test_backfill_blog_html.py -v`
Expected: all PASS.

- [ ] **Step 14.5: Commit**

```bash
git add scripts/__init__.py scripts/backfill_blog_html.py tests/test_backfill_blog_html.py
git commit -m "feat(scripts): add backfill_blog_html with dry-run + streaming-buffer retry"
```

---

### Task 15: Backfill — dry-run review, then real

**Files:** posts in `assets/blogs/` (lint may rewrite some)

- [ ] **Step 15.1: Run dry-run**

```bash
python scripts/backfill_blog_html.py --dry-run 2>&1 | tee /tmp/backfill-dryrun.log
```
Expected: 22 posts processed, summary shows 22 succeeded / 0 hard-failed.

- [ ] **Step 15.2: Inspect lint diffs**

The dry-run runs `_payload_from_blog`, which writes lint fixes back to the `.md` file. After dry-run, review what changed:

```bash
git status assets/blogs/
git diff assets/blogs/ | less
```

Spot-check a few diffs:
- Entity replacements (e.g. `&mdash;` → `—`) should be the bulk on legacy posts (0001-0020).
- No prose changes — lint only touches SVG content and named entities.

If diffs look surprising, investigate before continuing. Restore the file with `git checkout assets/blogs/<file>` and dig in.

- [ ] **Step 15.3: Commit lint-cleaned posts**

```bash
git add assets/blogs/
git commit -m "chore(blogs): apply lint fixes from backfill dry-run"
```

- [ ] **Step 15.4: Run real backfill**

```bash
python scripts/backfill_blog_html.py 2>&1 | tee /tmp/backfill-run.log
```

Expected: each post is updated. Posts inserted within the last ~30 min hit the streaming-buffer path; the script sleeps 35 min and retries. End-state: `succeeded: 22, hard-failed: 0`.

If the run hits hard failures, review the log, fix the underlying issue, and re-run for just the failed posts (e.g. `python -m src.cli blog update assets/blogs/<name>.md`).

- [ ] **Step 15.5: Verify in BigQuery**

```bash
bq query --nouse_legacy_sql \
  'SELECT COUNT(*) AS n_total, COUNTIF(body_html IS NOT NULL AND LENGTH(body_html) > 0) AS n_with_html FROM `noble-office-299208.portfolio.gn-blog`'
```
Expected: `n_total == n_with_html` and equal to the number of posts.

---

## Phase 5: Reader cutover

### Task 16: Add `body_html` to `Project` model

**Files:**
- Modify: `src/models/project.py`
- Add: `tests/test_project_model.py` (if it doesn't already exist; otherwise extend the existing tests file)

- [ ] **Step 16.1: Write failing test**

`tests/test_project_model.py` (or extend existing):
```python
"""Tests for src.models.project."""
from src.models.project import Project


def test_project_from_dict_reads_body_html():
    data = {
        "id": "x",
        "title": "T",
        "description": "d",
        "image": "https://e.com/i.svg",
        "tags": ["t"],
        "disabled": False,
        "views": 0,
        "likes": 0,
        "date": "2026-01-01T00:00:00Z",
        "body": "# md",
        "body_html": "<h1>md</h1>",
    }
    p = Project.from_dict(data)
    assert p.body_html == "<h1>md</h1>"
    assert p.body == "# md"  # transitional: both fields populated


def test_project_from_dict_defaults_body_html_to_empty_string():
    """A row that doesn't have body_html (legacy/transitional) yields an empty string."""
    data = {"id": "x", "title": "T", "description": "d", "image": "i", "body": "md"}
    p = Project.from_dict(data)
    assert p.body_html == ""
```

- [ ] **Step 16.2: Run tests**

Run: `pytest tests/test_project_model.py -v`
Expected: 1+ fail (no `body_html` field).

- [ ] **Step 16.3: Add `body_html` to the dataclass**

In `src/models/project.py`:

```python
@dataclass
class Project:
    id: str
    blog_id: str
    title: str
    description: str
    image: str
    tags: List[str] = field(default_factory=list)
    disabled: bool = False
    views: int = 0
    likes: int = 0
    date: str = ""
    body: str = ""           # legacy markdown source; dropped after the body column is dropped
    body_html: str = ""      # rendered HTML; the new source for the renderer
    slug: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        # ...existing tag and slug logic...
        return cls(
            id=data.get("id", ""),
            blog_id=data.get("blog_id", ""),
            title=title,
            description=data.get("description", ""),
            image=data.get("image", ""),
            tags=tags,
            disabled=data.get("disabled", False),
            views=data.get("views", 0),
            likes=data.get("likes", 0),
            date=data.get("date", ""),
            body=data.get("body", ""),
            body_html=data.get("body_html", ""),
            slug=slug,
        )
```

- [ ] **Step 16.4: Run tests**

Run: `pytest tests/test_project_model.py tests/ -v`
Expected: all PASS.

- [ ] **Step 16.5: Commit**

```bash
git add src/models/project.py tests/test_project_model.py
git commit -m "feat(models): Project gains body_html field for rendered HTML"
```

---

### Task 17: Switch `projects_page.py` renderer to use `body_html`

**Files:**
- Modify: `src/features/projects/projects_page.py:54`

- [ ] **Step 17.1: Make the change**

In `src/features/projects/projects_page.py`, line 54:
```python
# before
render_md(project.body),
# after
NotStr(project.body_html) if project.body_html else render_md(project.body),
```

Why the conditional: it's a defensive fallback so a row missing `body_html` (e.g. if someone manually inserts a row in the BQ console without going through the CLI) doesn't render as a blank page. Once we DROP the `body` column at task 20, the fallback is removed.

- [ ] **Step 17.2: Add an integration test**

In `tests/test_blog_detail_view.py` (new file):
```python
"""Tests that the blog detail page reads body_html in preference to body."""
from src.models.project import Project


def test_blog_detail_uses_body_html_when_present(monkeypatch):
    """Renderer prefers body_html when populated."""
    from src.features.projects import projects_page

    project = Project(
        id="x", blog_id="x", title="T", description="d", image="i",
        body="# markdown", body_html="<h1>html-rendered</h1>",
    )
    out = projects_page._render_blog_detail(project)
    rendered = str(out)
    assert "html-rendered" in rendered
    assert "# markdown" not in rendered  # markdown text not exposed raw


def test_blog_detail_falls_back_to_body_when_html_missing():
    """Renderer falls back to render_md(body) when body_html is empty."""
    from src.features.projects import projects_page

    project = Project(
        id="x", blog_id="x", title="T", description="d", image="i",
        body="# markdown", body_html="",
    )
    out = projects_page._render_blog_detail(project)
    rendered = str(out)
    # render_md should have produced an <h1> from the markdown.
    assert "<h1" in rendered
```

- [ ] **Step 17.3: Run tests**

Run: `pytest tests/test_blog_detail_view.py tests/ -v`
Expected: all PASS.

- [ ] **Step 17.4: Verify against the live site**

```bash
# Restart the dev server (or wait for cloud-run redeploy) and curl one post:
curl -s 'https://gabriel.navarro.bio/blogs/slug/portello-making-global-assembly-more-effective-for-rare-disease-whole-genome-sequencing' \
  | grep -c '<svg ' \
  # Expect ≥ 5 — the SVGs are now baked from body_html.
```

If you have Playwright access, run a quick check that no `<p><svg` appears in the rendered DOM.

- [ ] **Step 17.5: Commit**

```bash
git add src/features/projects/projects_page.py tests/test_blog_detail_view.py
git commit -m "feat(blog-detail): render body_html in preference to body"
```

---

### Task 18: Soak — 1 week of monitoring

**Files:** none

- [ ] **Step 18.1: Wait at least 7 days**

During the soak window:
- Watch the live site for any reports of broken posts.
- Spot-check a handful of posts manually each day.
- If a regression is found, the rollback is one revert: `git revert <task-17-commit>`.

- [ ] **Step 18.2: After 7 days, run a final sanity scan**

```bash
# Pull every blog row's body_html and assert validate_html returns clean.
python - <<'PY'
from src.services.projects import ProjectService
from src.services.blog_render import validate_html

projects = ProjectService().get_all_projects(include_disabled=True)
bad = [(p.id, p.title, validate_html(p.body_html)) for p in projects if validate_html(p.body_html)]
if bad:
    for pid, title, issues in bad:
        print(f"{pid} | {title}")
        for i in issues:
            print(f"  {i.kind}: {i.snippet[:100]}")
    raise SystemExit(1)
print(f"All {len(projects)} posts pass validate_html.")
PY
```
Expected: no output of bad rows; final line confirms all posts clean.

- [ ] **Step 18.3: Document the soak**

Append to the spec:

```markdown
**Soak log:**
- YYYY-MM-DD — soak began (commit <hash>).
- YYYY-MM-DD — soak ended; all 22 posts pass validate_html; no incidents reported.
```

```bash
git add docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md
git commit -m "docs(spec): record successful 1-week soak of body_html cutover"
```

---

## Phase 6: Drop legacy `body` column

### Task 19: DROP `body` column

**Files:** none (BigQuery DDL)

- [ ] **Step 19.1: Run the DDL**

```bash
bq query --nouse_legacy_sql \
  'ALTER TABLE `noble-office-299208.portfolio.gn-blog` DROP COLUMN body;'
```

- [ ] **Step 19.2: Verify**

```bash
bq show --schema --format=prettyjson noble-office-299208:portfolio.gn-blog | grep -c '"name": "body"'
```
Expected: `0` (only `body_html` remains; `body` is gone).

- [ ] **Step 19.3: Smoke-test live page**

Visit one blog post URL in a browser. The page should render exactly as before — `body_html` is the source.

- [ ] **Step 19.4: Document**

Append to spec under "Migration log":
```markdown
- YYYY-MM-DD — `ALTER TABLE ... DROP COLUMN body;` executed; verified via `bq show`.
```

```bash
git add docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md
git commit -m "chore(bq): drop legacy body column from gn-blog"
```

---

### Task 20: Remove transitional code

**Files:**
- Modify: `src/services/blog_frontmatter.py` (remove `body: str` from `BlogRow`)
- Modify: `src/cli/blog.py` (`_payload_from_blog` excludes `body` from BlogRow construction)
- Modify: `src/models/project.py` (remove `body` field)
- Modify: `src/features/projects/projects_page.py` (remove the `if project.body_html else render_md(project.body)` fallback)
- Modify: tests that asserted both fields (update to body_html only)

- [ ] **Step 20.1: Update tests first (red-green)**

Update `tests/test_blog_frontmatter.py` and `tests/test_project_model.py` so that:
- `BlogRow` test no longer passes `body=`.
- `Project` test no longer asserts `p.body`.
- `Project.from_dict` test passes a row dict with NO `body` key.

Also remove the fallback test in `tests/test_blog_detail_view.py`:
- Drop `test_blog_detail_falls_back_to_body_when_html_missing`.

- [ ] **Step 20.2: Run tests; expect failures in production code**

Run: `pytest tests/ -v`
Expected: failures in tests that touched `body`; production code still has the field.

- [ ] **Step 20.3: Remove the `body` field from production code**

In `src/services/blog_frontmatter.py` `BlogRow`:
```python
class BlogRow(BaseModel):
    """The shape of a row in the BigQuery `gn-blog` table.

    The legacy `body` column was dropped on YYYY-MM-DD; only `body_html`
    is stored.
    """
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    date: datetime
    tags: list[str]
    description: str
    image: HttpUrl
    type: Literal["note", "article"]
    disabled: bool
    views: int
    likes: int
    body_html: str
    # ...validator unchanged
```

In `src/cli/blog.py` `_payload_from_blog`:
```python
row = BlogRow(**{**blog.model_dump(exclude={"body"}), "body_html": html})
```

In `src/models/project.py` `Project`:
```python
@dataclass
class Project:
    # ...
    body_html: str = ""
    # body field REMOVED
    slug: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        # ...
        return cls(
            # ...
            body_html=data.get("body_html", ""),
            # body=...  REMOVED
            slug=slug,
        )
```

In `src/features/projects/projects_page.py`:
```python
NotStr(project.body_html),
```
(remove the conditional fallback).

- [ ] **Step 20.4: Run all tests**

Run: `pytest tests/ -v`
Expected: all PASS.

- [ ] **Step 20.5: Smoke test the CLI**

```bash
python -m src.cli blog validate assets/blogs/0021-portello.md
python -m src.cli blog submit assets/blogs/0021-portello.md --dry-run
```
Expected: both succeed; the dry-run JSON contains `body_html` and NO `body` key.

- [ ] **Step 20.6: Smoke-test live**

Visit any blog post in a browser. Expect identical rendering to before.

- [ ] **Step 20.7: Commit**

```bash
git add src/services/blog_frontmatter.py src/cli/blog.py src/models/project.py src/features/projects/projects_page.py tests/
git commit -m "refactor: remove transitional body field after legacy column drop"
```

---

## Phase 7: Documentation alignment

### Task 21: Update the paper-to-blog skill docs

**Files:**
- Modify: `.claude/skills/paper-to-blog/SKILL.md`
- Modify: `.claude/skills/paper-to-blog/references/blog_format.md`

These are informational-only changes — the skill's *workflow* hasn't changed (authors still write `.md` files). What changes is what `submit` does under the hood.

- [ ] **Step 21.1: Add a "Pipeline" subsection to SKILL.md**

After the existing "Stage 4: Fact and logic validation pass" section, add:

```markdown
## How submit works under the hood

`python -m src.cli blog submit <post.md>` runs an automated pipeline before
inserting into BigQuery:

1. **Lint** — auto-fixes mistletoe foot-guns: HTML named entities → Unicode,
   multi-line `<svg>` opens → single-line, blank lines inside SVG → stripped.
   Lint fixes are written back to the `.md` file. See
   `src/services/blog_lint.py`.
2. **Render** — `monsterui.render_md(body)` produces the final HTML.
3. **Validate** — scans the HTML for known bad patterns (no `<p><svg`, every
   SVG has `<title>` and `role="img"`, etc.). Submit fails if any issue is
   found. See `src/services/blog_render.py`.
4. **Submit** — inserts a row with `body_html` (rendered) into BigQuery. The
   live page reads `body_html` directly; mistletoe is not run at view time.

If submit reports a `[lint]` line, your `.md` was edited; commit the diff.
If submit reports a `[error]` line, the lint couldn't auto-fix something
(e.g. an unmapped HTML entity, or an SVG without a `<title>`); fix the
source and re-run.
```

- [ ] **Step 21.2: Note the change in `blog_format.md`**

Add to the top:

```markdown
## Server-side rendering (since 2026-05)

Blog posts are rendered to HTML at submit time and stored in BigQuery as
`body_html`. The `.md` file in `assets/blogs/` remains the editable
source. See `docs/superpowers/specs/2026-04-30-blog-html-pipeline-design.md`.

Authors do not need to do anything different: write the `.md`, run
`python -m src.cli blog submit ...`. The pipeline lints, renders, and
validates automatically.
```

- [ ] **Step 21.3: Commit**

```bash
git add .claude/skills/paper-to-blog/SKILL.md .claude/skills/paper-to-blog/references/blog_format.md
git commit -m "docs(skill): document body_html pipeline in paper-to-blog skill"
```

---

## Acceptance Criteria (per spec)

The migration is complete when:

- [ ] `python -m src.cli blog submit <any-post.md>` succeeds with linted source written back to disk and `body_html` populated in BigQuery.
- [ ] All 22 existing posts have non-null `body_html` in the table.
- [ ] Every public blog page renders without a `<p><svg` or `<p><text` pattern in the served HTML (verify with curl + grep, or Playwright).
- [ ] The `body` column has been dropped from `gn-blog` (verify with `bq show --schema`).
- [ ] `pytest tests/test_blog_lint.py tests/test_blog_render.py tests/test_blog_pipeline_e2e.py tests/test_backfill_blog_html.py tests/test_cli_blog.py tests/test_blog_frontmatter.py tests/test_project_model.py tests/test_blog_detail_view.py` passes (a single full `pytest tests/` run also works).
- [ ] The paper-to-blog skill's `SKILL.md` and `references/blog_format.md` mention the new pipeline.

---

## Self-review (recorded after first pass)

- **Spec coverage:** Every numbered item in spec's "Implementation order" maps to a task: schema add → 13, lint → 1-6, render → 7-8, BlogRow → 9, payload wiring → 10-11, backfill dry-run + run → 14-15, reader → 16-17, soak → 18, drop → 19, transitional cleanup → 20. Skill docs (acceptance criterion #6) → task 21.
- **Placeholder scan:** Searched for TBD/TODO; none. Every code step shows full code.
- **Type consistency:** `LintFix.kind` literal values match between `blog_lint.py` and tests. `ValidationIssue.kind` literal values match between `blog_render.py` and tests. `BlogRow` field names match across the model, `_payload_from_blog`, and tests. `Project` field names match across the dataclass, `from_dict`, the renderer call, and tests.
- **Scope check:** Single migration. One implementation plan. No further decomposition needed.
- **Ambiguity check:** "Soak" is explicitly defined as ≥ 7 days plus a final sanity scan. "Streaming buffer retry" is explicitly 35 min, single retry. "Transitional code removal" lists every file.
