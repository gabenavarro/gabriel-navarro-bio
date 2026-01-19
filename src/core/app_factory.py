from fasthtml.common import *
from monsterui.all import *

def create_app():
    """
    Creates and configures the FastHTML application.
    """
    app, rt = fast_app(
        hdrs=(
            Theme.slate.headers(highlightjs=True),
            Favicon("/assets/ico/favicon.ico", "/assets/ico/favicon.ico"),
        ),
        title="Gabriel, PhD",
    )
    return app, rt
