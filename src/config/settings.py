"""
Centralized application configuration.

This module contains all application settings including BigQuery config,
UI constants, color schemes, and content for the hero page.
"""

import logging
import os

logger = logging.getLogger(__name__)


class Settings:
    """Application settings and configuration.

    Convention: env-derived settings live as instance attributes set in
    `__init__` so they re-read the environment on each construction (useful
    for tests). UI/content constants stay as class attributes.
    """

    def __init__(self) -> None:
        # ============================================================================
        # Google Cloud Platform Configuration
        # ============================================================================
        self.GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "noble-office-299208")
        self.BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE", "noble-office-299208.portfolio.gn-blog")
        logger.info(
            "GCP project: %s, BigQuery table: %s",
            self.GOOGLE_PROJECT_ID,
            self.BIGQUERY_TABLE,
        )

    # ============================================================================
    # Navigation & Social Links
    # ============================================================================
    NAV_LINKS = [
        {"label": "Projects", "href": "/projects"},
        {"label": "Blogs", "href": "/blogs"},
        {"label": "CV", "href": "/cv"},
    ]

    SOCIAL_LINKS = [
        {"label": "LinkedIn", "href": "https://www.linkedin.com/in/gcnavarro/"},
        {"label": "GitHub", "href": "https://github.com/gabenavarro"},
        {"label": "Email", "href": "mailto:gchinonavarro@gmail.com"},
    ]

    # ============================================================================
    # Category Mapping
    # ============================================================================
    CATEGORY_MAP = {
        "bioinformatics": "omics",
        "genomics": "omics",
        "transcriptomics": "omics",
        "metabolomics": "omics",
        "proteomics": "omics",
        "protein folding": "machine-learning",
        "machine learning": "machine-learning",
        "deep-learning": "machine-learning",
        "state-space-models": "machine-learning",
        "flashattention": "machine-learning",
        "transformers": "machine-learning",
        "webdevelopment": "visualization",
        "html": "visualization",
        "css": "visualization",
        "javascript": "visualization",
        "docker": "infrastructure",
        "cloud": "infrastructure",
        "gcp": "infrastructure",
    }

    # ============================================================================
    # Hero Skills & Descriptions
    # ============================================================================
    HERO_SKILLS = [
        "Computational Scientist",
        "Machine Learning Researcher",
        "Bioinformatician",
        "Synthetic Chemist",
    ]

    HERO_SKILLS_DESCRIPTION = {
        "Bioinformatician": "I decode complex biological datasets to uncover hidden insights and accelerate scientific breakthroughs. Let's transform data into discoveries together!",
        "Data Engineer": "I build robust, scalable pipelines that efficiently handle petabyte-scale datasets. Let's turn massive data into actionable insights together!",
        "Computational Scientist": "I employ cutting-edge computational methods to solve challenging scientific problems. Let's push the boundaries of research together!",
        "Machine Learning Researcher": "I design and deploy machine learning models that extract valuable patterns from data. Let's unlock new possibilities with AI together!",
        "Cloud Architect": "I create scalable, secure cloud infrastructures that power high-performance computing. Let's innovate in the cloud together!",
        "Python Developer": "I craft efficient, maintainable Python solutions that simplify complex tasks. Let's build powerful applications together!",
        "Database Specialist": "I design high-performance databases to store and retrieve vast amounts of information. Let's make data instantly accessible together!",
        "Genomics Expert": "I analyze genomic sequences to reveal key biological insights and drive scientific progress. Let's decode life's blueprint together!",
        "Metabolomics Scientist": "I map and interpret metabolic pathways to identify health-impacting compounds. Let's explore the chemistry of life together!",
        "Mass Spectrometrist": "I harness advanced mass spectrometry techniques to detect and quantify complex molecules. Let's unveil the secrets in every sample together!",
        "Software Engineer": "I develop reliable, efficient software systems to tackle intricate problems at scale. Let's code extraordinary solutions together!",
        "Technical Mentor": "I guide teams through complex technical challenges, fostering growth and innovation. Let's develop tomorrow's experts together!",
        "Team Leader": "I motivate and coordinate diverse teams to achieve ambitious goals. Let's build a culture of success together!",
        "Research Scientist": "I conduct rigorous experiments and analyses to drive scientific advancements. Let's make groundbreaking discoveries together!",
        "Problem Solver": "I excel at dissecting tough technical issues, delivering smart, efficient solutions. Let's transform obstacles into opportunities together!",
        "Agile Practitioner": "I champion iterative development and continuous collaboration to adapt and innovate. Let's deliver top-quality results together!",
        "Systems Integrator": "I piece together complex software components into a seamless whole. Let's create cohesive technology ecosystems together!",
        "Project Manager": "I orchestrate plans, people, and resources to finish projects on time and under budget. Let's bring big ideas to life together!",
        "Documentation Expert": "I create clear, comprehensive documentation to bridge technical and non-technical audiences. Let's keep everyone on the same page together!",
        "Cross-Functional Expert": "I thrive at the intersection of disciplines, uniting diverse teams to solve multifaceted problems. Let's drive impactful collaboration together!",
        "Synthetic Chemist": "I design and synthesize novel compounds to advance scientific research. Let's innovate in the lab together!",
    }

    # ============================================================================
    # Hero Page Content
    # ============================================================================
    HERO_CONTENT = {
        "greeting": "Hi, I'm Gabriel Navarro, PhD ",
        "portrait_url": "https://storage.googleapis.com/gn-portfolio/images/portriat.png",
        "default_skill": "Computational Scientist",
        "default_description": """I am a computational scientist who loves building tools that help biologists do amazing science.

I spent the past decade bridging machine learning and biology by training genome language models, fine-tuning protein models for antibody design, and creating platforms that turned terabytes of messy omics data into actual discoveries.

These days I'm all about creating scalable, cloud-native tools that make complex biology accessible. Whether that's through interactive dashboards, automated genomics workflows, or full-stack web apps. I geek out on making science faster and more intuitive, one pipeline at a time.

Let's push the boundaries of research together!""",
        "about_sections": [
            {
                "title": "Experienced Computational Scientist",
                "items": [
                    {
                        "subtitle": "Cross-Disciplinary Expertise",
                        "text": "Over a decade of experience at the intersection of biology, chemistry, and machine learning—spanning **metabolomics**, **proteomics**, **genomics**, and **drug discovery**.",
                    },
                    {
                        "subtitle": "Industry-Backed Innovation",
                        "text": "Led high-impact projects at global companies and startups, including **Datacca**, **Triplebar**, **Brightseed**, **Amyris**, **Hexagon Bio**, and **Mondelez**, building platforms used by R&D and commercial teams.",
                    },
                    {
                        "subtitle": "Scientific Rigor & Engineering Precision",
                        "text": "Combines deep scientific knowledge with advanced software and cloud engineering to turn raw biological data into scalable, actionable systems.",
                    },
                ],
                "button": {"text": "My Curriculum Vitae", "href": "/cv"},
            },
            {
                "title": "Machine Learning in Biosciences",
                "items": [
                    {
                        "subtitle": "Genome Language Models",
                        "text": "Trained and fine-tuned fungal genome language models to optimize **protein expression and secretion**, accelerating synthetic biology applications.",
                    },
                    {
                        "subtitle": "Protein Language Models",
                        "text": "Fine-tuned antibody-specific PLMs to enhance **sequence design** with demonstrably improved functional outcomes",
                    },
                    {
                        "subtitle": "Molecule Fingerprints from Mass Spectrometry",
                        "text": "Developed machine learning models that mapped 20,000+ plant compounds to human health outcomes, driving a **1000x increase** in phytonutrient discovery throughput.",
                    },
                    {
                        "subtitle": "Fungal Compound Discovery",
                        "text": "Designed and deployed scalable workflows on Google Cloud Vertex AI using GATK, samtools, Dragen-OS, and other bioinformatics tools to streamline genomic analysis at scale.",
                    },
                ],
                "button": {
                    "text": "My Machine Learning Projects",
                    "href": "/projects?tag=machine-learning",
                },
            },
            {
                "title": "Omics Infrastructure & Pipelines",
                "subsections": [
                    {
                        "title": "🧫 Genomics",
                        "items": [
                            {
                                "subtitle": "Scalable DNA Processing",
                                "text": "Designed and deployed scalable workflows on Google Cloud Vertex AI using GATK, samtools, Dragen-OS, and other bioinformatics tools to streamline genomic analysis at scale.",
                            }
                        ],
                    },
                    {
                        "title": "🧪 Proteomics",
                        "items": [
                            {
                                "subtitle": "End-to-End Proteomics Platform",
                                "text": "Built a comprehensive proteomics pipeline supporting the entire research workflow—from benchside experimentation to insights-driven decision-making by scientists.",
                            }
                        ],
                    },
                    {
                        "title": "🧉 Metabolomics",
                        "items": [
                            {
                                "subtitle": "Scalable DNA Processing",
                                "text": "Developed high-throughput metabolomics pipelines capable of processing terabyte-scale LC-MS/MS datasets for accelerated discovery.",
                            }
                        ],
                    },
                ],
                "button": {"text": "My Omics Projects", "href": "/projects?tag=omics"},
            },
            {
                "title": "Data Science & Visualization",
                "items": [
                    {
                        "subtitle": "Multi-Omics Platform for R&D",
                        "text": "Built interactive Python Dash and FastHTML dashboards to empower scientists to explore complex datasets and extract actionable insights across multi-omics domains.",
                    }
                ],
                "button": {
                    "text": "My Visualization Projects",
                    "href": "/projects?tag=visualization",
                },
            },
            {
                "title": "Infrastructure & Scalability",
                "items": [
                    {
                        "subtitle": "Cloud Bioinformatics",
                        "text": "Architected and deployed scalable, production-ready infrastructure to support AI/ML-driven genome and antibody design workflows in cloud environments.",
                    }
                ],
                "button": {
                    "text": "My Infrastructure Projects",
                    "href": "/projects?tag=infrastructure",
                },
            },
        ],
    }


# Singleton instance
settings = Settings()


# ============================================================================
# Category -> CSS class mapping
# ============================================================================
# Single source of truth for the actual color values lives in CSS:
# `--cat-omics`, `--cat-ml`, `--cat-infra`, `--cat-viz`, `--cat-neutral`
# (defined in `src/styles/_base.py`). This mapping only chooses which class
# to apply to a given tag string.
_CATEGORY_TAG_TO_CLASS = {
    "omics": "cat-omics",
    "genomics": "cat-omics",
    "bioinformatics": "cat-omics",
    "ml": "cat-ml",
    "machine-learning": "cat-ml",
    "ai": "cat-ml",
    "infrastructure": "cat-infra",
    "infra": "cat-infra",
    "docker": "cat-infra",
    "devops": "cat-infra",
    "visualization": "cat-viz",
    "viz": "cat-viz",
    "ui": "cat-viz",
}


def category_class(tag: str) -> str:
    """Map a tag to its CSS category class. Falls back to 'cat-neutral' for unknowns."""
    return _CATEGORY_TAG_TO_CLASS.get(tag.lower().strip(), "cat-neutral")
