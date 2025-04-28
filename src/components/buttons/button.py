from fasthtml.common import A, Style

_css = """
.button-container {
    margin-top: 2rem;
}

.btn {
    display: inline-block;
    padding: 0.8rem 1.8rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
}

.btn-primary {
    background: var(--primary-color);
    color: var(--black);
    border: 2px solid var(--primary-color);
}

.btn-primary:hover {
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: var(--white);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(106, 91, 255, 0.3);
}

.btn-outline {
    background: transparent;
    color: var(--white);
    border: 2px solid #444;
}

.btn-outline:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}


/* Small screens */
@media (max-width: 768px) {

    
    .btn {
        width: 100%;
    }

    .stats-container {
        flex-wrap: wrap;
        margin-top: 2rem;
        gap: 1.5rem;
        justify-content: space-between;
    }
}

"""

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
    return A(text, Style(_css), href=href, _class="btn btn-primary")


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
        Style(_css), 
        href=href, 
        cls="btn btn-outline" + (" open-modal-btn" if modal_open else ""),
    )