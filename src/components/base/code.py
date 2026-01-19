from fasthtml.common import *
from monsterui.all import *

def FactoryCodeBlock(code, lang="python"):
    """Renders a code block with the Factory technical aesthetic."""
    return Div(
        # Header bar
        Div(
            Div(
                cls="factory-code-header-dash"
            ),  # Simulating the dash via CSS or content
            UkIcon("copy", cls="factory-code-copy", uk_tooltip="Copy to clipboard"),
            cls="factory-code-header",
        ),
        # Code Body
        Div(
            CodeBlock(code, lang=lang, cls="factory-code-body", code_cls="shiki"),
            cls="factory-code-content",
        ),
        cls="factory-code-container",
    )
