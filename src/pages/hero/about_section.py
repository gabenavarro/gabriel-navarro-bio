from fasthtml.common import Style, Div, H1, Span, P, Button, Img, H2, A, Section, Ul, Li, Strong
from src.components.backgrounds import transition_js_css

ABOUT_ME = Div(
    Section(
        H2("🧑‍🔬 10+ Years in Computational Science"),
        Ul(
            Li(
                Div(Strong("Cross-Disciplinary Expertise", cls="primary-color")),
                "Over a decade of experience at the intersection of biology, chemistry, and machine learning—spanning ",
                Strong("metabolomics"), ", ",
                Strong("proteomics"), ", ",
                Strong("genomics"), ", and ", 
                Strong("drug discovery"), "."
            ),
            Li(
                Div(Strong("Industry-Backed Innovation", cls="primary-color")),
                "Led high-impact projects at global companies and startups, including ",
                Strong("Datacca"), ", ",
                Strong("Triplebar"), ", ",
                Strong("Brightseed"), ", ",
                Strong("Amyris"), ", ",
                Strong("Hexagon Bio"), ", and ", 
                Strong("Mondelez"), ", building platforms used by R&D, regulatory, and commercial teams."
            ),
            Li(
                Div(Strong("Scientific Rigor & Engineering Precision", cls="primary-color")),
                "Combines deep scientific knowledge with advanced software and cloud engineering to turn raw biological data into scalable, actionable systems.",
            )
        )
    )
)