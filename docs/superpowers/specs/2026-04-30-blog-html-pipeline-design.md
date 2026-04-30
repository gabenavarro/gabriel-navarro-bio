# Blog HTML Pipeline — Design

**Date:** 2026-04-30
**Status:** Approved (Option B from brainstorming)
**Owner:** Gabriel Navarro
**Author of spec:** Claude (paper-to-blog brainstorming session)

## Problem

The portfolio's blog system stores raw markdown in BigQuery and renders it server-side at view time via `monsterui.render_md` (which calls `mistletoe.markdown` under the hood). This works fine for prose-heavy posts but has produced three distinct rendering bugs in posts containing inline SVG diagrams:

1. **HTML named entities in SVG content** (`&mdash;`, `&middot;`, `&times;`, `&rarr;`). SVG is XML and only the five XML-predefined entities (`&amp; &lt; &gt; &apos; &quot;`) parse. Anything else breaks XML parsing. Fix: replace with Unicode literals.
2. **Multi-line `<svg ...>` opening tags.** Mistletoe's CommonMark Type-7 HTML-block detection requires the entire opening tag to fit on one line; multi-line attributes mean the parser doesn't recognize the SVG as a block, wraps it in a `<p>`, and the browser's HTML5 parser self-closes the empty `<svg>` immediately, leaving every child as orphan DOM. Fix: collapse opening tag to one line.
3. **Blank lines inside `<svg>` blocks followed by single-line elements.** Mistletoe terminates HTML blocks at blank lines. When the next non-blank line is `<text x="220" y="74">Train positions</text>` (single-line element with content directly after the opening tag's `>`), the parser's "any other tag" rule rejects it (because the opening tag isn't followed by whitespace or end-of-line), falls back to paragraph parsing, and wraps the line in `<p>...</p>`. The matching `</svg>` ends up nested inside another `<p>`. Fix: strip blank lines inside SVG blocks.

All three bugs share a single root cause: **mistletoe parses SVG content as markdown, which it isn't designed for.** Each instance is mechanically fixable, but reactively patching every new mistletoe foot-gun is friction. As of 2026-04-30, post `0022-spike-sparse-sink-anatomy-massive.md` had 33 sites where mistletoe wrapped SVG content in `<p>` tags before the bug class was identified.

## Goals

- Move the markdown→HTML render from view time to submit time.
- Store the final HTML in BigQuery; the `.md` file remains the editable source.
- Surface mistletoe foot-guns at submit time (when they're cheap to fix), not at view time (when they're already live).
- Backfill all 22 existing posts so the cutover is clean.
- Drop the legacy `body` (markdown) column from BigQuery once verified.

## Non-goals

- Restructuring the body as typed JSON blocks (Option C from brainstorming). Considered, rejected as over-engineering for ≤30 posts.
- Replacing mistletoe with a different markdown renderer.
- Changing the markdown frontmatter format (still legacy `@{...}` blocks per `blog_format.md`).
- Re-authoring existing posts. Lint may rewrite SVG content but will not change prose.

## Architecture

```
            ┌──────────────────────────────┐
            │ /app/assets/blogs/NNNN-x.md  │  ← source of truth (markdown)
            └──────────────┬───────────────┘
                           │  python -m src.cli blog submit ...
                           ▼
   ┌───────────────────────────────────────────────────────┐
   │ _payload_from_blog()                                  │
   │  1. ensure_id(path)        — backfill UUID            │
   │  2. parse_blog(path)        — Pydantic-validate .md   │
   │  3. lint_body(body)         — auto-fix mistletoe      │
   │       • entity replacement                            │
   │       • single-line SVG open                          │
   │       • strip blank lines in SVG                      │
   │       • write fixes back to .md                       │
   │  4. render_to_html(body)    — mistletoe + classes     │
   │  5. validate_html(html)     — fail-loud on bad shapes │
   │  6. emit BlogRow {id, ..., body_html}                 │
   └─────────────────────┬─────────────────────────────────┘
                         │
                         ▼
   ┌───────────────────────────────────────────────────────┐
   │ BigQuery: noble-office-299208.portfolio.gn-blog       │
   │   id | title | date | tags | description | image     │
   │   type | disabled | views | likes | body_html        │
   └─────────────────────┬─────────────────────────────────┘
                         │
                         ▼
   ┌───────────────────────────────────────────────────────┐
   │ Page render (FastHTML route /blogs/slug/<slug>)       │
   │   ProjectService.get_project_by_slug(slug) → Project  │
   │   _render_blog_detail(project):                       │
   │     ...                                               │
   │     NotStr(project.body_html)                         │
   │     ...                                               │
   └───────────────────────────────────────────────────────┘
```

The `.md` file remains the editable source. Mistletoe runs once at submit time. The lint step auto-fixes the three known mistletoe foot-guns and writes the cleaned source back to disk so the `.md` and the BigQuery HTML stay in sync.

## Components

### New module: `src/services/blog_lint.py`

Pure-Python, no I/O coupling. Exposes:

```python
@dataclass
class LintFix:
    kind: Literal["named-entity", "multi-line-svg-open", "blank-line-in-svg"]
    count: int        # how many sites the rule fixed
    detail: str       # short human-readable summary

def lint_body(body: str) -> tuple[str, list[LintFix]]: ...
```

Order of operations within `lint_body`:
1. Replace named entities (preserving the five XML-safe ones).
2. Collapse multi-line `<svg ...>` opening tags.
3. Strip blank lines inside `<svg>...</svg>` blocks.

Each step uses a regex with `re.DOTALL` and is idempotent (safe to run twice). The lint **does not** touch:
- Fenced code blocks (` ``` ` to ` ``` `): protect with a "stash and restore" pre/post pass.
- Inline code (single backticks): same.
- Markdown prose outside `<svg>` blocks: blanks lines in prose are intentional paragraph breaks.
- HTML-comment-only lines outside SVG.

Unmapped entities raise `LintError` with the unmapped entity name. The CLI catches this and prints a clear "add mapping for `&copy;` and re-run" message.

### New module: `src/services/blog_render.py`

Bridges the linted markdown to validated HTML:

```python
@dataclass
class ValidationIssue:
    kind: Literal["p-wraps-svg", "svg-tag-mismatch", "svg-missing-title", "svg-missing-role"]
    line: int | None
    snippet: str

def render_to_html(body: str) -> str: ...
def validate_html(html: str) -> list[ValidationIssue]: ...
```

`render_to_html` calls `monsterui.render_md(body, ...)` to keep the existing class-mapping behavior (Tailwind `text-lg leading-relaxed mb-6` on paragraphs, etc.). The function unwraps the `NotStr`/`FT` and returns a plain string.

`validate_html` runs four checks (see "Validation rules" below). Returns `[]` on success.

### Modified module: `src/services/blog_frontmatter.py`

Add a new Pydantic model that represents the BigQuery row payload (distinct from the file-level `BlogFrontmatter`):

```python
class BlogRow(BaseModel):
    """The shape of a row in the BigQuery `gn-blog` table.

    During migration (steps 2-9) this model carries both `body` and
    `body_html`; the CLI populates both on every submit/update. After
    step 10 drops the `body` column, the field is removed from this
    model and its callers.
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
    body: str          # legacy markdown source; dropped at step 10
    body_html: str     # rendered HTML; the new source of truth for the renderer

    @field_validator("body_html")
    @classmethod
    def _body_html_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("body_html must be non-empty")
        return value
```

`BlogFrontmatter` (representing the on-disk `.md` file) keeps its existing `body: str` field — that's the markdown source.

### Modified module: `src/cli/blog.py`

`_payload_from_blog(path)` rewires to:

```python
def _payload_from_blog(path: Path) -> dict[str, Any]:
    blog = parse_blog(path)                     # BlogFrontmatter
    fixed, fixes = lint_body(blog.body)
    if fixes:
        _persist_lint_fixes(path, fixed)        # write back to .md
        for f in fixes:
            print(f"[lint] {f.kind}: {f.detail} (×{f.count})")
    html = render_to_html(fixed)
    issues = validate_html(html)
    if issues:
        for i in issues:
            print(f"[error] {i.kind}: {i.snippet[:120]} (line {i.line})", file=sys.stderr)
        raise ValueError(f"validate_html found {len(issues)} issue(s)")
    row = BlogRow(**{**blog.model_dump(), "body_html": html})
    return row.model_dump(mode="json")
```

Note that `blog.body` (the linted markdown) and `html` (rendered) are both written during the migration period. After step 10, `BlogRow.body` is removed; `_payload_from_blog` adjusts to `{**blog.model_dump(exclude={"body"}), "body_html": html}`.

`_cmd_validate` is upgraded to also run `lint` + `render_to_html` + `validate_html` and print issues — but it does NOT write back to disk or push anywhere. Pure read-only check. (Useful for `pre-commit`-style local verification.)

`_cmd_submit` and `_cmd_update` are unchanged in flow — they just consume the new `body_html` payload.

### Modified module: `src/services/projects.py`

`Project` model gains `body_html: str` (alongside the existing `body: str` for the legacy column during migration). After the `body` column is dropped, `body` is removed from the model.

### Modified module: `src/features/projects/projects_page.py`

Single line change:
```python
# before
render_md(project.body),
# after
NotStr(project.body_html),
```

### New script: `scripts/backfill_blog_html.py`

One-time backfill runner. Usage:

```bash
python scripts/backfill_blog_html.py --dry-run     # preview every change
python scripts/backfill_blog_html.py               # execute
```

Iterates `assets/blogs/*.md` in numeric order, runs `_payload_from_blog` on each, and calls `python -m src.cli blog update <path>` (or the equivalent in-process). Stops on first failure (non-zero exit) so partial migrations are visible. Reports a summary at the end: posts processed, lint fixes applied per post, validation issues (should be 0).

The script handles the streaming-buffer constraint by:
1. Submitting all updates in a tight loop first.
2. Catching streaming-buffer errors per-post.
3. After the loop, sleeping 35 minutes and retrying any that failed.
4. Failing hard if a row still can't be updated after the second attempt.

## Validation rules

Implemented in `validate_html`:

1. **`p-wraps-svg`** — no `<p>` element directly precedes any of `<svg`, `<text`, `<rect`, `<line`, `<circle`, `<path`, `<g`, `<defs`, `<marker`, `<!--`. This is the exact diagnostic signature of the class-3 bug.
2. **`svg-tag-mismatch`** — count of `<svg ` opening tags equals count of `</svg>` closing tags. Drift indicates parser state corruption.
3. **`svg-missing-title`** — every top-level `<svg>...</svg>` block contains at least one direct-child `<title>` element. "Top-level" means the SVG is at column 0 of the rendered HTML or the immediate child of a structural container (`<div>`, `<details>`); not nested inside another `<svg>`. Some templates put `<defs>` before `<title>`, so we don't require `<title>` to be the *first* child — we require it to be a child.
4. **`svg-missing-role`** — every top-level `<svg ` opening tag has `role="img"`. Same definition of "top-level" as above.

All four are runnable on the rendered HTML string with regex; no DOM library required.

## Edge cases

- **Indented SVGs inside CSS-widget containers** (`ptb-step-mds`, `ptb-step-hd`). These are inside `<div>...</div>` blocks which mistletoe passes through verbatim. Lint should skip them — the regex for "blank line inside SVG" only matches when the surrounding `<svg>` is at column 0 (top-level), not when indented. (Cleaner: skip any SVG whose preceding non-blank line is `<div ...>` or that's inside a `<div>` block.)
- **Code blocks containing SVG examples** (e.g. tutorials about SVG). Stash fenced code blocks before lint, restore after. The skill's `references/svg_diagrams.md` itself contains code-block SVG examples; the lint must not mangle those.
- **Greek letters and trademark symbols** (`&alpha;`, `&copy;`, etc.). The entity map covers these. If a new symbol appears, the lint fails loud with "add mapping for X" rather than silently passing through.
- **Markdown emphasis inside SVG `<text>`** (`<text>**bold**</text>`). Mistletoe doesn't currently emphasize-parse content inside HTML blocks, so this passes through. Regression test included.
- **Bare `<` and `>` inside SVG `<text>`** (e.g. `<text>x &lt; 5</text>`). These render fine. Lint leaves them alone.

## Testing

New file: `tests/test_blog_lint.py`. One test per bug class plus idempotency:

```python
def test_lint_replaces_named_entities()
def test_lint_collapses_multi_line_svg_open()
def test_lint_strips_blank_lines_inside_svg()
def test_lint_is_idempotent()
def test_lint_skips_fenced_code_blocks()
def test_lint_skips_indented_widget_svgs()
def test_lint_fails_on_unmapped_entity()
```

New file: `tests/test_blog_render.py`:

```python
def test_render_to_html_passes_clean_input_through()
def test_validate_html_returns_empty_for_clean_html()
def test_validate_html_catches_p_wrapping_svg()
def test_validate_html_catches_missing_title()
def test_validate_html_catches_missing_role_img()
def test_validate_html_catches_tag_mismatch()
```

Integration: `tests/test_blog_pipeline_e2e.py`:

```python
def test_pipeline_on_real_post_0022()  # canary: post that originally had the bug
def test_pipeline_on_real_post_0020()  # control: a post without SVGs
def test_pipeline_writes_lint_fixes_back()
```

The pytest harness should already exist (per `CLAUDE.md`: "Backend: pytest + httpx"). New tests slot in.

## Schema migration

BigQuery doesn't allow column renames, so the migration is `ADD body_html` → backfill → switch reader → `DROP body`.

### Steps in order

1. **Add `body_html` column.**
   ```sql
   ALTER TABLE `noble-office-299208.portfolio.gn-blog`
   ADD COLUMN body_html STRING;
   ```
   The Pydantic model reading rows still uses `body`; the new column is dormant.

2. **Ship the CLI changes.** New posts populate `body_html`. `body` continues to be populated via the existing markdown body field on `BlogFrontmatter` for transitional reads. (Concretely: `_payload_from_blog` writes BOTH `body` (markdown) AND `body_html` (rendered) for the duration of the migration.)

3. **Backfill all 22 posts** via `scripts/backfill_blog_html.py`. After this completes, every row has `body_html`.

4. **Switch the reader.** `_render_blog_detail` changes to `NotStr(project.body_html)`. `Project.body_html` becomes required, `Project.body` becomes optional (transitional).

5. **Soak for 1 week.** Live page now serves `body_html`. If a regression appears, easy rollback: revert step 4.

6. **Drop the `body` column.**
   ```sql
   ALTER TABLE `noble-office-299208.portfolio.gn-blog`
   DROP COLUMN body;
   ```
   `Project.body` and `BlogRow` no longer reference it. `_payload_from_blog` stops writing it.

### Migration risks

- **Streaming-buffer constraint on `update`.** Each `update` is DELETE+INSERT, and the streaming buffer holds rows for ~30 min. Backfilling 22 posts naively will trip this. The backfill script handles it with a 35-minute retry loop.
- **Lint rewrites legacy posts.** Posts 0001–0020 were authored before the lint rules existed. The lint will likely modify some of them (entity replacements, blank-line stripping). The script runs a `--dry-run` mode first; user reviews the diff before pushing.
- **Step 4 → step 5 cutover.** Once the reader switches, the old `body` column is no longer rendered. If `body_html` is somehow corrupted on a post, the page goes blank. Mitigation: the `validate_html` step at submit guarantees no row gets `body_html=""` or malformed HTML.
- **Existing CI/deploy pipeline.** No changes needed — `_cmd_submit` is the only entry point and it's still the same command. CI doesn't run `blog submit`.

## Error handling summary

| Stage | Failure | Surface |
|---|---|---|
| Lint | unmapped entity | `LintError`; CLI prints "add mapping for X" + offending file:line; non-zero exit |
| Render | mistletoe raises | wrap in `RenderError` with surrounding 3 lines; non-zero exit |
| Validate | any issue | print all issues to stderr; non-zero exit; do NOT push |
| Submit | streaming buffer | print user-friendly "row in streaming buffer; retry in 30 min"; non-zero exit |
| Backfill | one post fails | log it, continue with the rest; final summary lists failures |

## Out of scope (for follow-ups)

- A `blog rebuild-html` CLI command that re-renders all posts in place (useful if mistletoe or monsterui ever update with new behavior).
- Caching the rendered HTML at the application layer (already implicit — BigQuery row reads are cheap and cacheable upstream).
- Linting the `references/svg_diagrams.md` examples themselves to verify the templates produce clean HTML (low priority — those are demonstrative, not user-facing).
- A `pre-commit` hook that runs `blog validate` on touched `.md` files (nice-to-have).

## Acceptance criteria

The migration is complete when:

1. `python -m src.cli blog submit <any-post.md>` succeeds with linted source written back to disk and `body_html` populated in BigQuery.
2. All 22 existing posts have non-null `body_html` in the table.
3. Every public blog page renders without a `<p><svg` or `<p><text` pattern in the served HTML.
4. The `body` column has been dropped from `gn-blog`.
5. `pytest tests/test_blog_lint.py tests/test_blog_render.py tests/test_blog_pipeline_e2e.py` passes.
6. The paper-to-blog skill's `SKILL.md` and references are updated to reference the new pipeline (informational; the skill workflow doesn't change for authors).

## Implementation order (high-level — full plan via writing-plans)

1. Add `body_html` column (BigQuery DDL).
2. Implement `blog_lint.py` + tests.
3. Implement `blog_render.py` + tests.
4. Add `BlogRow` Pydantic model.
5. Wire `_payload_from_blog` to lint+render+validate; populate both `body` and `body_html`.
6. Implement and run `backfill_blog_html.py --dry-run`; review diff.
7. Run `backfill_blog_html.py` for real.
8. Update `Project` model + `projects_page.py` to read `body_html`.
9. Soak 1 week.
10. Drop `body` column; remove transitional code.

The detailed step-by-step plan lives in the implementation plan that `writing-plans` produces from this spec.
