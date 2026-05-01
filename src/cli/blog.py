"""Blog subcommands for the ``src.cli`` CLI.

Provides ``validate``, ``submit``, ``update``, ``disable``, and ``list``
operations against the BigQuery-backed blog table. Parsing and validation
use :mod:`src.services.blog_frontmatter`; BigQuery writes use the official
``google.cloud.bigquery`` SDK (the project's lightweight REST client only
supports queries, not row inserts).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from src.config.settings import settings
from src.services.blog_frontmatter import BlogRow, ensure_id, parse_blog
from src.services.blog_lint import LintError, lint_body
from src.services.blog_render import RenderError, render_to_html, validate_html
from src.services.projects import ProjectService

logger = logging.getLogger(__name__)


def register_blog_parser(p: argparse.ArgumentParser) -> None:
    """Attach the ``blog`` subcommands to the given parser."""
    sub = p.add_subparsers(dest="blog_cmd", required=True)

    v = sub.add_parser("validate", help="Parse and validate a markdown file's frontmatter")
    v.add_argument("path", type=Path, help="Path to the markdown file")

    s = sub.add_parser("submit", help="Insert a new blog post into BigQuery")
    s.add_argument("path", type=Path, help="Path to the markdown file")
    s.add_argument("--dry-run", action="store_true", help="Print the payload without inserting")
    s.add_argument("--table", default=None, help="Override settings.BIGQUERY_TABLE")

    u = sub.add_parser("update", help="Upsert a blog post (delete by id then insert)")
    u.add_argument("path", type=Path, help="Path to the markdown file")
    u.add_argument("--dry-run", action="store_true", help="Print planned operations only")
    u.add_argument("--table", default=None, help="Override settings.BIGQUERY_TABLE")

    d = sub.add_parser("disable", help="Mark a blog post as disabled")
    d.add_argument("id", help="The blog post id (UUID)")
    d.add_argument("--table", default=None, help="Override settings.BIGQUERY_TABLE")

    lst = sub.add_parser(
        "list",
        help="List blog posts (id, title, disabled flag). --table is currently ignored.",
    )
    lst.add_argument("--all", action="store_true", help="Include disabled posts")
    lst.add_argument(
        "--table",
        default=None,
        help="Reserved for future use; currently ignored (uses settings.BIGQUERY_TABLE)",
    )


def run_blog(args: argparse.Namespace) -> int:
    """Dispatch the parsed ``blog`` subcommand."""
    if args.blog_cmd == "validate":
        return _cmd_validate(args)
    if args.blog_cmd == "submit":
        return _cmd_submit(args)
    if args.blog_cmd == "update":
        return _cmd_update(args)
    if args.blog_cmd == "disable":
        return _cmd_disable(args)
    if args.blog_cmd == "list":
        return _cmd_list(args)
    return 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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
        raise ValueError(f"validate_html found {len(issues)} issue(s); fix the source and re-run")

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


def _bq_client():  # pragma: no cover - thin wrapper around external SDK
    """Construct a ``google.cloud.bigquery.Client`` from the env credentials."""
    from google.cloud import bigquery

    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path:
        return bigquery.Client.from_service_account_json(creds_path)
    return bigquery.Client()


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


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


def _cmd_submit(args: argparse.Namespace) -> int:
    try:
        ensure_id(args.path)
        payload = _payload_from_blog(args.path)
    except Exception as exc:  # noqa: BLE001
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    table = args.table or settings.BIGQUERY_TABLE

    if args.dry_run:
        print(f"[dry-run] would insert into {table}:")
        print(json.dumps(payload, indent=2, default=str))
        return 0

    client = _bq_client()
    errors = client.insert_rows_json(table, [payload])
    if errors:
        print(f"insert failed: {errors}", file=sys.stderr)
        return 1
    print(f"submitted {payload['id']} to {table}")
    return 0


def _cmd_update(args: argparse.Namespace) -> int:
    try:
        ensure_id(args.path)
        payload = _payload_from_blog(args.path)
    except Exception as exc:  # noqa: BLE001
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    table = args.table or settings.BIGQUERY_TABLE
    post_id = payload["id"]

    if args.dry_run:
        print(f"[dry-run] would DELETE FROM `{table}` WHERE id = '{post_id}'")
        print(f"[dry-run] then INSERT into {table}:")
        print(json.dumps(payload, indent=2, default=str))
        return 0

    from google.cloud import bigquery

    client = _bq_client()
    delete_sql = f"DELETE FROM `{table}` WHERE id = @id"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", post_id)]
    )
    client.query(delete_sql, job_config=job_config).result()
    errors = client.insert_rows_json(table, [payload])
    if errors:
        print(f"insert failed after delete: {errors}", file=sys.stderr)
        return 1
    print(f"updated {post_id} in {table}")
    return 0


def _cmd_disable(args: argparse.Namespace) -> int:
    table = args.table or settings.BIGQUERY_TABLE

    from google.cloud import bigquery

    client = _bq_client()
    sql = f"UPDATE `{table}` SET disabled = true WHERE id = @id"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", args.id)]
    )
    client.query(sql, job_config=job_config).result()
    print(f"disabled {args.id}")
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    if args.table:
        print(
            "warning: --table is ignored on list; uses settings.BIGQUERY_TABLE",
            file=sys.stderr,
        )
    posts = ProjectService().get_all_projects(include_disabled=args.all)
    for post in posts:
        flag = "disabled" if post.disabled else "enabled"
        print(f"{post.id}\t{post.title}\t{flag}")
    return 0
