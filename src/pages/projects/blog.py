from fasthtml.common import Style, Div
from typing import List, Dict
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MarkedJS
from src.lib.google.bigquery import BigQueryClient


css = """
/* marked test section */
.marked {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

.centered-not-found {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    text-align: center;
    font-size: 1.5rem;
    color: var(--dark-newspaper-bg);
}

"""


def blog_div_from_blog(blog: List[Dict]):
    """ Example of a section with Marked.js for Markdown parsing."""
    return Div(
        "No blog found",
        cls="centered-not-found"
    ) if not blog else Div(
        blog[0]["body"],
        cls="marked"
    )

def create_blog_page(uuid: str):
    """ Create a blog page with a specific UUID. """
    client = BigQueryClient()
    blog = client.query(sql="SELECT * FROM `noble-office-299208.portfolio.gn-blog` WHERE id = @uuid", params={"uuid": uuid})
    blog_div = blog_div_from_blog(blog)
    return Div(
        Style(ROOT_CSS + BODY_CSS + css),
        MarkedJS(),
        NAVIGATION,
        Div(style="height: 10vh;"),
        blog_div,
        cls="container"
    )