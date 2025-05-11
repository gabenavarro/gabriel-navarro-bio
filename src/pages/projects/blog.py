from fasthtml.common import Style, Div, Script
from typing import List, Dict
from src.components import simple_navigation, contact_me_modal
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

/*!
  Theme: Default
  Description: Original highlight.js style
  Author: (c) Ivan Sagalaev <maniac@softwaremaniacs.org>
  Maintainer: @highlightjs/core-team
  Website: https://highlightjs.org/
  License: see project LICENSE
  Touched: 2021
*/pre code.hljs{display:block;overflow-x:auto;padding:1em}code.hljs{padding:3px 5px}.hljs{background:#f3f3f3;color:#444}.hljs-comment{color:#697070}.hljs-punctuation,.hljs-tag{color:#444a}.hljs-tag .hljs-attr,.hljs-tag .hljs-name{color:#444}.hljs-attribute,.hljs-doctag,.hljs-keyword,.hljs-meta .hljs-keyword,.hljs-name,.hljs-selector-tag{font-weight:700}.hljs-deletion,.hljs-number,.hljs-quote,.hljs-selector-class,.hljs-selector-id,.hljs-string,.hljs-template-tag,.hljs-type{color:#800}.hljs-section,.hljs-title{color:#800;font-weight:700}.hljs-link,.hljs-operator,.hljs-regexp,.hljs-selector-attr,.hljs-selector-pseudo,.hljs-symbol,.hljs-template-variable,.hljs-variable{color:#ab5656}.hljs-literal{color:#695}.hljs-addition,.hljs-built_in,.hljs-bullet,.hljs-code{color:#397300}.hljs-meta{color:#1f7199}.hljs-meta .hljs-string{color:#38a}.hljs-emphasis{font-style:italic}.hljs-strong{font-weight:700}

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
        simple_navigation(),
        contact_me_modal(),
        Div(style="height: 10vh;"),
        blog_div,
        cls="container"
    )