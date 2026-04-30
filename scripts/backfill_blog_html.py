"""Backfill body_html for every blog post in /app/assets/blogs.

Usage:
    python scripts/backfill_blog_html.py --dry-run   # preview only
    python scripts/backfill_blog_html.py             # execute (one update per post)

In execute mode, each post is processed:
  1. Run _payload_from_blog (lint -> render -> validate) and persist any lint fixes
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
            print(
                f"[dry-run] would update id={payload.get('id', '?')} "
                f"(body_html: {len(payload.get('body_html', ''))} chars)"
            )
            successes.append(path)
            continue

        ns = Namespace(path=path, dry_run=False, table=None)
        try:
            rc = blog_module._cmd_update(ns)
        except Exception as exc:  # noqa: BLE001
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
        print(
            f"\n=== Sleeping 35 minutes before retrying "
            f"{len(streaming_failures)} streaming-buffer post(s) ==="
        )
        time.sleep(35 * 60)
        for path in streaming_failures:
            print(f"\n--- retry: {path.name} ---")
            ns = Namespace(path=path, dry_run=False, table=None)
            try:
                rc = blog_module._cmd_update(ns)
            except Exception as exc:  # noqa: BLE001
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only; do not push to BigQuery.",
    )
    parser.add_argument(
        "--blogs-dir",
        default=str(DEFAULT_BLOGS_DIR),
        help="Directory containing the blog .md files.",
    )
    args = parser.parse_args(argv)
    return run_backfill(Path(args.blogs_dir), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
