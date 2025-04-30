from fasthtml.common import Style, Script, Div, H2, H3, Section, Ul, Li, Strong
from src.components.backgrounds import transition_js_css, glow_object
from src.components.buttons import button_outline

transition_css, transition_js = transition_js_css("about-background")
glow_3 = glow_object(3, 40, 22)
glow_4 = glow_object(4, 10, 88)
glow_5 = glow_object(5, 34, 68)
glow_6 = glow_object(6, 73, 34)
glow_7 = glow_object(7, 95, 14)

_css = transition_css + """

.about-background {
    height: 100%;
    width: 100%;
    display: flex;
    position: relative;
    background-color: transparent;
    z-index: 1;
}

.about-block {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 80vh;
    padding: 2rem;
}

.about-block-right-aligned {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    padding-right: 4rem;
}

""" + glow_3 + glow_4 + glow_5 + glow_6 + glow_7


ABOUT_ME = Div(
    Script(transition_js),
    Style(_css),

    # Years experience
    Div(
        Section(
            Div(
                H2("Experienced Computational Scientist", cls="section-title scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Cross-Disciplinary Expertise", cls="secondary-color subtitle")),
                        "Over a decade of experience at the intersection of biology, chemistry, and machine learning—spanning ",
                        Strong("metabolomics"), ", ",
                        Strong("proteomics"), ", ",
                        Strong("genomics"), ", and ", 
                        Strong("drug discovery"), ".",
                        cls="scroll-left-hidden"
                    ),
                    Li(
                        Div(Strong("Industry-Backed Innovation", cls="secondary-color subtitle")),
                        "Led high-impact projects at global companies and startups, including ",
                        Strong("Datacca"), ", ",
                        Strong("Triplebar"), ", ",
                        Strong("Brightseed"), ", ",
                        Strong("Amyris"), ", ",
                        Strong("Hexagon Bio"), ", and ", 
                        Strong("Mondelez"), ", building platforms used by R&D and commercial teams.",
                        cls="scroll-left-hidden"
                    ),
                    Li(
                        Div(Strong("Scientific Rigor & Engineering Precision", cls="secondary-color subtitle")),
                        "Combines deep scientific knowledge with advanced software and cloud engineering to turn raw "
                        "biological data into scalable, actionable systems.",
                        cls="scroll-left-hidden"
                    )
                )
            ),
            Div(
                button_outline("My Curriculum Vitae", href="/cv"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),
    
        # Machine Learning
        Section(
            Div(
                H2("Machine Learning in Biosciences", cls="section-title scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Molecule Fingerprints from Mass Spectrometry", cls="secondary-color subtitle")),
                        "Developed machine learning models that mapped 20,000+ plant compounds to human health outcomes, driving a ",
                        Strong("1000x increase"), " in phytonutrient discovery throughput.",
                        cls="scroll-left-hidden"
                    ),
                    Li(
                        Div(Strong("Fungal Compound Discovery", cls="secondary-color subtitle")),
                        "Designed and deployed scalable workflows on Google Cloud Vertex AI using GATK, samtools, "
                        "Dragen-OS, and other bioinformatics tools to streamline genomic analysis at scale.",
                        cls="scroll-left-hidden"
                    )
                )
            ),
            Div(
                button_outline("My Machine Learning Projects", href="/projects"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),

        Section(
            Div(
                H2("AI in Genomics & Protein Design", cls="section-title scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Genome Language Models", cls="secondary-color subtitle")),
                        "Trained and fine-tuned fungal genome language models to optimize ",
                        Strong("protein expression and secretion"), ", accelerating synthetic biology applications.",
                        cls="scroll-left-hidden"
                    ),
                    Li(
                        Div(Strong("Protein Language Models", cls="secondary-color subtitle")),
                        "Fine-tuned antibody-specific PLMs to enhance ",
                        Strong("sequence design"), " with demonstrably improved functional outcomes",
                        cls="scroll-left-hidden"
                    )
                )
            ),
            Div(
                button_outline("My AI Projects", href="/projects"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),


        Section(
            Div(
                H2("Omics Infrastructure & Pipelines", cls="section-title scroll-left-hidden"),
                
                H3("🧫 Genomics", cls="scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Scalable DNA Processing", cls="secondary-color subtitle")),
                        "Designed and deployed scalable workflows on Google Cloud Vertex AI using GATK, samtools, Dragen-OS, "
                        "and other bioinformatics tools to streamline genomic analysis at scale.",
                        cls="scroll-left-hidden"
                    ),
                ),

                H3("🧪 Proteomics", cls="scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("End-to-End Proteomics Platform", cls="secondary-color subtitle")),
                        "Built a comprehensive proteomics pipeline supporting the entire research workflow—from benchside "
                        "experimentation to insights-driven decision-making by scientists.",
                        cls="scroll-left-hidden"
                    ),
                ),

                H3("🧉 Metabolomics", cls="scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Scalable DNA Processing", cls="secondary-color subtitle")),
                        "Developed high-throughput metabolomics pipelines capable of processing terabyte-scale ",
                        "LC-MS/MS datasets for accelerated discovery.",
                        cls="scroll-left-hidden"
                    ),
                )
            ),
            Div(
                button_outline("My Omics Projects", href="/projects"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),

        Section(
            Div(
                H2("Data Science & Visualization", cls="section-title scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Multi-Omics Platform for R&D", cls="secondary-color subtitle")),
                        "Built interactive Python Dash and FastHTML dashboards to empower scientists to explore complex "
                        "datasets and extract actionable insights across multi-omics domains.",
                        cls="scroll-left-hidden"
                    ),
                )
            ),
            Div(
                button_outline("My Visualization Projects", href="/projects"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),

        Section(
            Div(
                H2("Infrastructure & Scalability", cls="section-title scroll-left-hidden"),
                Ul(
                    Li(
                        Div(Strong("Cloud Bioinformatics", cls="secondary-color subtitle")),
                        "Architected and deployed scalable, production-ready infrastructure to support AI/ML-driven "
                        "genome and antibody design workflows in cloud environments.",
                        cls="scroll-left-hidden"
                    ),
                )
            ),
            Div(
                button_outline("My Infrastructure Projects", href="/projects"),
                cls="scroll-right-hidden about-block-right-aligned"
            ),
            cls="about-block"
        ),

        cls="container"
    ),
    Div(cls="glow-1"),
    Div(cls="glow-2"),
    Div(cls="glow-3"),
    Div(cls="glow-4"),
    Div(cls="glow-5"),
    Div(cls="glow-6"),
    Div(cls="glow-7"),
    Div(cls="particles-container", id="particles-container"),
    cls="about-background"
)