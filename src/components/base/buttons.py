"""Shared button primitives used across the portfolio.

The three helpers (`button_primary`, `button_outline`, `button_ghost`) are the
canonical way to render CTAs. They emit consistent class names that map to
`.factory-btn` plus a variant class in `src/styles/_components.py`, so call
sites stay free of inline ``style=`` attributes.

When ``href`` is provided, the helper renders as ``<a>`` (anchor); otherwise it
renders as ``<button>`` (form button).
"""

from fasthtml.common import A, Button


def _classes(variant: str, extra: str) -> str:
    """Compose the class string: factory-btn + factory-btn-{variant} + extra."""
    parts = ["factory-btn", f"factory-btn-{variant}"]
    if extra:
        parts.append(extra)
    return " ".join(parts)


def button_primary(label: str, href: str | None = None, cls: str = "", **kwargs):
    """Solid primary button: white bg on dark."""
    class_str = _classes("primary", cls)
    if href is not None:
        return A(label, href=href, cls=class_str, **kwargs)
    return Button(label, cls=class_str, **kwargs)


def button_outline(label: str, href: str | None = None, cls: str = "", **kwargs):
    """Outlined button: transparent bg, accent border."""
    class_str = _classes("outline", cls)
    if href is not None:
        return A(label, href=href, cls=class_str, **kwargs)
    return Button(label, cls=class_str, **kwargs)


def button_ghost(label: str, href: str | None = None, cls: str = "", **kwargs):
    """Text-only ghost button: accent color, no bg, used for inline CTAs like '← RETURN'."""
    class_str = _classes("ghost", cls)
    if href is not None:
        return A(label, href=href, cls=class_str, **kwargs)
    return Button(label, cls=class_str, **kwargs)
