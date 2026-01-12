from fasthtml.common import A, Style
from src.lib.css import BUTTON_CSS


def button_primary(text: str, href: str) -> A:
    """Primary Button
    ---

    Creates a primary button with the given text and href.

    ### Args:
        * text (str): The text to display on the button.
        * href (str): The URL to link to when the button is clicked.

    ### Returns:
        A: An anchor element representing the button.
    """
    return A(text, Style(BUTTON_CSS), href=href, _class="btn btn-primary")


def button_outline(text: str, href: str, modal_open: bool = False) -> A:
    """Secondary Button
    ---

    Creates an outline button with the given text and href.

    ### Args:
        * text (str): The text to display on the button.
        * href (str): The URL to link to when the button is clicked.
        * id (str, optional): The optional ID for the button element.

    ### Returns:
        A: An anchor element representing the button.
    """
    return A(
        text,
        Style(BUTTON_CSS),
        href=href,
        cls="btn btn-outline" + (" open-modal-btn" if modal_open else ""),
    )
