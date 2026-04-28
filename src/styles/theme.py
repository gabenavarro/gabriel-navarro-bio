"""Deprecated: theme variables now live in `src/styles/_base.py`.

`THEME_CSS` is kept as an empty string for backwards compatibility with
existing imports (`src/components/layout/page.py`, `src/styles/__init__.py`).
All color tokens — including `--cat-omics`, `--cat-ml`, `--cat-infra`,
`--cat-viz`, `--cat-neutral`, `--primary-color`, `--secondary-color`,
`--white`, and `--black` — are defined in `_base.py`'s `:root` block.
"""

THEME_CSS = ""
