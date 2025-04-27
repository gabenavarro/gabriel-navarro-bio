from fasthtml.common import Style, Div, Script, Img, H1, H3, P
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MasonryJS, MarkedJS
from typing import Optional
from src.lib.google.bigquery import BigQueryClient
import random


MAX_CARD_WIDTH = 250

css = """
.masonry-container {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

.masonry-card {
    background-color: var(--dark-newspaper-bg);
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    padding: 0.75rem;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}

.masonry-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: transform 0.3s ease;
    z-index: 3;
    background-color: var(--dark-highlight-newspaper);
    color: var(--white);
    text-decoration: none;
    filter: brightness(1.05);

}

.masonry-sizer {
    max-width: 250px;

    /* Medium screens */
    @media (max-width: 992px) {
        max-width: 400px;
    }

    /* Small screens */
    @media (max-width: 768px) {
        max-width: 600px;
    }
}

.rounded-img {
    width: 100%;
    height: auto;
    border-radius: 5px;
}

/* marked test section */
.marked {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

"""
rando = random.Random()

def generate_cards(tag:Optional[str] = None):
    """ Create a card with an image, title, and description."""
    client = BigQueryClient()
    blogs = client.query(sql="SELECT * FROM `noble-office-299208.portfolio.gn-blog` LIMIT 1000")
    
    return Div(
        *[
            Div(
                Img(
                    src=entry["image"], 
                    alt=f"",
                    cls="rounded-img",
                ),
                H3(entry["title"], cls="white"),
                P(entry["description"], cls="white"),
                cls="masonry-card masonry-sizer"
            ) for entry in blogs],
        cls="masonry-container",
    )


# TODO: Move this to bigquery for blog posts and for cards
# def marked_section():
#     """ Example of a section with Marked.js for Markdown parsing."""
#     return Div(
#         """
# # Mastering Quality Control in Omics with FastQC

# Quality control (QC) of sequencing data is a foundational step in bioinformatics workflows, crucial for ensuring reliable and accurate results in omics analyses. Among the many available tools, **FastQC** has emerged as an industry-standard software for performing quality assessments of FASTQ files.

# ### Basic Usage Example

# Running FastQC on single-end reads:

# ```bash
# fastqc sample.fastq -o output_directory
# ```

# - `sample.fastq`: The FASTQ file to be assessed.
# - `-o`: Specifies the directory for output reports.

# For paired-end data:

# ```bash
# fastqc sample_R1.fastq sample_R2.fastq -o output_directory
# ```

# ## Interpreting FastQC Reports

# FastQC reports use traffic-light indicators:

# - 🟢 **Pass**: The metric falls within an acceptable range.
# - 🟡 **Warn**: Potential issues; requires careful interpretation.
# - 🔴 **Fail**: Significant quality issues that require intervention.

# ## Conclusion

# FastQC remains indispensable in modern bioinformatics, providing clear, actionable insights into sequencing data quality. Integrating FastQC into your omics workflows helps ensure robust and reliable data analysis outcomes.

# Happy sequencing and quality checking!
#         """,
#         cls="marked"
#     )


def create_blog_page():
    return Div(
        Style(ROOT_CSS + BODY_CSS + css),
        MasonryJS(
            sel=".masonry-container",
            item_selector=".masonry-card",
            column_width=".masonry-sizer",
            gutter=20,
            percent_position=False,
            horizontal_order=True,
            origin_left=True,
            origin_top=True,
        ),
        MarkedJS(),
        NAVIGATION,
        Div(style="height: 10vh;"),
        Div(
            generate_cards(),
        ),
        cls="container",
    )



MASONRY_PAGE = create_blog_page()