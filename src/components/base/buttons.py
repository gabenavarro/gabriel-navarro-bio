from fasthtml.common import A, Style
from src.styles import BUTTON_CSS

def button_primary(text: str, href: str) -> A:
    """Primary Factory-style button."""
    return A(text, Style(BUTTON_CSS), href=href, cls="btn btn-primary")

def button_outline(text: str, href: str, modal_open: bool = False) -> A:
    """Outline Factory-style button."""
    return A(
        text,
        Style(BUTTON_CSS),
        href=href,
        cls="btn btn-outline" + (" open-modal-btn" if modal_open else ""),
    )
