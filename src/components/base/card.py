"""Shared Card primitive used across the portfolio."""

from fasthtml.common import A, Div


_PADDING_CLASSES = {
    "sm": "factory-card-padding-sm",
    "md": "factory-card-padding-md",
    "lg": "factory-card-padding-lg",
}


def Card(
    *body,
    header=None,
    footer=None,
    href: str | None = None,
    padding: str = "md",
    interactive: bool = False,
    cls: str = "",
):
    """Render a card with optional header/footer; optionally clickable as a whole."""
    if padding not in _PADDING_CLASSES:
        raise ValueError(f"padding must be sm|md|lg; got {padding!r}")

    classes = ["factory-card", _PADDING_CLASSES[padding]]
    if interactive or href:
        classes.append("factory-card-interactive")
    if cls:
        classes.append(cls)
    class_str = " ".join(classes)

    children = []
    if header is not None:
        children.append(Div(header, cls="factory-card-header"))
    children.append(Div(*body, cls="factory-card-body"))
    if footer is not None:
        children.append(Div(footer, cls="factory-card-footer"))

    if href:
        return A(*children, href=href, cls=class_str)
    return Div(*children, cls=class_str)
