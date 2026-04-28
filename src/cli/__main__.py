"""Entry point for ``python -m src.cli``.

Dispatches to subcommand modules. ``blog`` is the only top-level command
today; future subcommands (e.g. project import/export) plug in here.
"""

from __future__ import annotations

import argparse
from typing import Sequence

from .blog import register_blog_parser, run_blog


def main(argv: Sequence[str] | None = None) -> int:
    """Parse ``argv`` and dispatch to the appropriate subcommand."""
    parser = argparse.ArgumentParser(prog="src.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)
    register_blog_parser(sub.add_parser("blog", help="Blog post operations"))
    args = parser.parse_args(argv)
    if args.cmd == "blog":
        return run_blog(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
