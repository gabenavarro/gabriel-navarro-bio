"""Blog frontmatter parser and pydantic schema.

This module is the single source of truth for parsing blog post markdown
files used by the portfolio. It supports two frontmatter formats:

1. **Legacy** ``@{key = value\\n  key2 = ["a","b"]\\n}`` blocks — the format
   currently in use across ``assets/blogs/``.
2. **Standard YAML** delimited by ``---`` lines on either side.

The public surface is intentionally tiny:

- :class:`BlogFrontmatter` — pydantic v2 model that validates the parsed
  metadata plus the markdown body.
- :func:`parse_blog` — read a file and return a validated
  :class:`BlogFrontmatter`.
- :func:`ensure_id` — backfill a UUID into a frontmatter block that is
  missing one, rewriting the file in place while preserving its format.
"""

from __future__ import annotations

import ast
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator


class BlogFrontmatter(BaseModel):
    """Validated frontmatter + body for a single blog post."""

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

    @field_validator("body")
    @classmethod
    def _body_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("body must be non-empty")
        return value


def _split_frontmatter(text: str) -> tuple[str, str, str]:
    """Detect the frontmatter format and return ``(format, frontmatter, body)``.

    ``format`` is one of ``"legacy"`` or ``"yaml"``. ``frontmatter`` is the
    raw text *between* the delimiters (excluding the delimiters themselves).
    ``body`` is everything after the closing delimiter, preserving line
    endings.
    """
    lines = text.splitlines(keepends=True)
    # Skip leading blank lines when sniffing the format.
    first_idx = next((i for i, ln in enumerate(lines) if ln.strip()), None)
    if first_idx is None:
        raise ValueError("File missing frontmatter; expected '@{...}' or '---' delimiter")

    first = lines[first_idx].lstrip()

    if first.startswith("@{"):
        end_idx = next(
            (i for i, ln in enumerate(lines) if i > first_idx and ln.strip() == "}"),
            None,
        )
        if end_idx is None:
            raise ValueError("Closing '}' for legacy frontmatter not found")
        # Strip leading "@{" from first line and trailing "}" from last line.
        inner_lines: list[str] = []
        head = lines[first_idx][len("@{") :]
        if head.strip():
            inner_lines.append(head)
        for ln in lines[first_idx + 1 : end_idx]:
            inner_lines.append(ln)
        return "legacy", "".join(inner_lines), "".join(lines[end_idx + 1 :])

    if first.startswith("---"):
        end_idx = next(
            (i for i, ln in enumerate(lines) if i > first_idx and ln.strip() == "---"),
            None,
        )
        if end_idx is None:
            raise ValueError("Closing '---' for YAML frontmatter not found")
        inner = "".join(lines[first_idx + 1 : end_idx])
        return "yaml", inner, "".join(lines[end_idx + 1 :])

    raise ValueError("File missing frontmatter; expected '@{...}' or '---' delimiter")


def _parse_legacy(frontmatter: str) -> dict[str, Any]:
    """Parse a legacy ``@{...}`` body into a dict."""
    metadata: dict[str, Any] = {}
    for raw in frontmatter.splitlines():
        line = raw.strip()
        if not line or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        try:
            metadata[key] = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            # Fall back to the raw string if literal_eval can't parse it.
            metadata[key] = val
    return metadata


def _parse_yaml(frontmatter: str) -> dict[str, Any]:
    """Parse YAML frontmatter into a dict.

    YAML errors are allowed to propagate; PyYAML errors include the
    offending line/column information.
    """
    data = yaml.safe_load(frontmatter)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must be a mapping at the top level")
    return data


def parse_blog(path: str | Path) -> BlogFrontmatter:
    """Parse a markdown blog post and return a validated :class:`BlogFrontmatter`."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    fmt, frontmatter, body = _split_frontmatter(text)
    data = _parse_legacy(frontmatter) if fmt == "legacy" else _parse_yaml(frontmatter)
    data["body"] = body
    return BlogFrontmatter(**data)


def _format_legacy_value(value: Any) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, list):
        return "[" + ", ".join(f'"{item}"' for item in value) + "]"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def ensure_id(path: Path) -> str:
    """Ensure the post at ``path`` has an ``id`` field; generate + persist if missing.

    Returns the id (existing or newly generated). The file is only rewritten
    when a new id is generated, and the original frontmatter format is
    preserved.
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    fmt, frontmatter, body = _split_frontmatter(text)
    data = _parse_legacy(frontmatter) if fmt == "legacy" else _parse_yaml(frontmatter)

    if "id" in data and isinstance(data["id"], str) and data["id"].strip():
        return data["id"]

    new_id = str(uuid.uuid4())
    data["id"] = new_id

    if fmt == "legacy":
        ordered = ["id"] + [k for k in data if k != "id"]
        out_lines: list[str] = []
        first_key = ordered[0]
        out_lines.append(f"@{{{first_key} = {_format_legacy_value(data[first_key])}\n")
        for key in ordered[1:]:
            if key == "tags":
                # Preserve the existing convention of writing tags as a bare
                # python-list repr (matches the pre-existing CLI behavior).
                out_lines.append(f"  {key} = {data[key]}\n")
            else:
                out_lines.append(f"  {key} = {_format_legacy_value(data[key])}\n")
        out_lines.append("}\n")
        p.write_text("".join(out_lines) + body, encoding="utf-8")
    else:
        ordered = {"id": new_id, **{k: v for k, v in data.items() if k != "id"}}
        dumped = yaml.safe_dump(ordered, sort_keys=False)
        p.write_text(f"---\n{dumped}---\n{body}", encoding="utf-8")

    return new_id
