from fasthtml.common import *
from monsterui.all import *


def cv_section_header(title):
    return Div(
        Div(title.upper(), cls="factory-label"),
        style="margin-top: 4rem; margin-bottom: 2rem;",
    )


def cv_experience():
    experiences = [
        {
            "title": "Head of Machine Learning and Bioinformatics",
            "company": "Triplebar",
            "period": "January 2024 — Present",
            "bullets": [
                "Designed and trained 2B-parameter genome language model on 4,000 fungal genomes using multi-node distributed training (16 GPUs), achieving 15% improvement in variant effect prediction.",
                "Fine-tuned 8B foundation models for genotype-phenotype prediction, implementing custom PyTorch workflows with gradient checkpointing and mixed-precision training.",
                "Applied protein structure prediction (Boltz, ESM) and diffusion-based design (RFDiffusion) to develop naïve antibody screening strategies, reducing costs by 40%.",
                "Architected cloud-native genomic analysis pipeline processing 200+ whole genomes weekly, reducing variant calling time from 72 to 2 hours using GATK and NVIDIA Parabricks on GCP Vertex AI.",
            ],
        },
        {
            "title": "Data Scientist III",
            "company": "Amyris",
            "period": "December 2021 — December 2023",
            "bullets": [
                "Built end-to-end multi-omics data platform integrating genomics, proteomics, and metabolomics for candidate gene identification.",
                "Developed unsupervised learning pipeline for metabolite clustering using dimensionality reduction (UMAP, t-SNE) and hierarchical clustering.",
                "Implemented automated feature extraction from mass spectrometry data using convolutional neural networks, achieving 92% accuracy in compound classification.",
            ],
        },
        {
            "title": "Senior Scientist, Computational Metabolomics",
            "company": "Hexagon Bio",
            "period": "March 2020 — November 2021",
            "bullets": [
                "Developed high-throughput metabolomics pipeline processing 4+ TB of LC-MS/MS data, reducing analysis time from weeks to days.",
                "Built deep learning models for retention time prediction and spectral matching, improving accuracy by 35%.",
                "Accelerated natural product discovery pipeline by 5x through integration of computational predictions with experimental validation.",
            ],
        },
        {
            "title": "Lead Scientist, Computational Metabolomics",
            "company": "Brightseed",
            "period": "February 2018 — February 2020",
            "bullets": [
                "Architected 'Forager' AI platform achieving 100x increase in phytonutrient identification throughput for 20,000+ compounds.",
                "Developed custom molecular fingerprinting and supervised learning models to identify 50+ novel bioactive molecules.",
                "Led initiatives connecting computational predictions to experimental design, resulting in 2 patent applications.",
            ],
        },
        {
            "title": "Senior Scientist, Mass Spectrometry Specialist",
            "company": "Mondelez International",
            "period": "January 2016 — January 2018",
            "bullets": [
                "Developed machine learning-based QC algorithms reducing mass spectrometry analysis time by 90% across 3 global manufacturing facilities.",
                "Implemented automated decision systems for real-time quality control at industrial scale.",
            ],
        },
    ]

    return Section(
        cv_section_header("Work Experience"),
        *[
            Div(
                Grid(cols=12)(
                    Div(
                        P(
                            exp["period"],
                            style="font-weight: 700; color: var(--color-base-500); font-size: 0.875rem;",
                        ),
                        cls="col-span-12 md:col-span-3",
                    ),
                    Div(
                        H3(
                            exp["title"].upper(),
                            style="margin-top: 0; color: var(--color-white); font-weight: 700; font-size: 1.125rem;",
                        ),
                        P(
                            exp["company"].upper(),
                            style="font-weight: 700; color: var(--color-accent-100); font-size: 0.75rem; margin-bottom: 1rem;",
                        ),
                        Ul(
                            *[
                                Li(
                                    b,
                                    style="color: var(--color-base-400); font-size: 0.875rem; margin-bottom: 0.5rem;",
                                )
                                for b in exp["bullets"]
                            ],
                            style="margin-top: 1rem; list-style-type: none; padding-left: 0;",
                        ),
                        cls="col-span-12 md:col-span-9",
                    ),
                ),
                style="margin-bottom: 3rem; padding: 2rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary);",
            )
            for exp in experiences
        ],
    )


def cv_education():
    edu = [
        {
            "degree": "Postdoctoral Researcher, IRACDA Fellow",
            "school": "University of California, San Diego",
            "period": "2014 — 2015",
        },
        {
            "degree": "PhD in Chemistry, NSF GRFP Fellow",
            "school": "University of California Santa Cruz",
            "period": "2008 — 2013",
        },
        {
            "degree": "Bachelor of Science in Chemical Biology",
            "school": "University of California Berkeley",
            "period": "2004 — 2008",
        },
    ]
    return Section(
        cv_section_header("Education"),
        *[
            Div(
                Grid(cols=12)(
                    Div(
                        P(
                            e["period"],
                            style="font-weight: 700; color: var(--color-base-500); font-size: 0.875rem;",
                        ),
                        cls="col-span-12 md:col-span-3",
                    ),
                    Div(
                        H3(
                            e["degree"].upper(),
                            style="margin-top: 0; color: var(--color-white); font-weight: 700; font-size: 1.125rem;",
                        ),
                        P(
                            e["school"].upper(),
                            style="font-weight: 700; color: var(--color-accent-100); font-size: 0.75rem;",
                        ),
                        cls="col-span-12 md:col-span-9",
                    ),
                ),
                style="margin-bottom: 2rem; padding: 2rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary);",
            )
            for e in edu
        ],
    )


def cv_skills():
    skills = {
        "Foundation Models & ML": [
            "Pre-training, fine-tuning, evaluation framework design",
            "Genomic & Protein Language Models (Evo2, ESM, Boltz)",
            "Diffusion Models (RFDiffusion) for antibody design",
            "Distributed training (DDP, FSDP, Megatron-LM), Multi-GPU clusters",
        ],
        "Computational Biology": [
            "Variant calling (GATK, Parabricks), Genome assembly",
            "LC-MS/MS analysis (targeted & untargeted), Antibody design",
            "Biological Databases: NCBI, UniProt, PDB, MassIVE",
            "Chemistry: RDKit, molecular fingerprinting, SAR analysis",
        ],
        "Software & Infrastructure": [
            "Python, R, SQL, Bash, JavaScript, Java",
            "PyTorch, Lightning, BioNeMo, Scikit-learn",
            "Cloud: GCP (Vertex AI), AWS, Docker, Kubernetes",
            "DevOps: Git, CI/CD, reproducible workflows",
        ],
    }

    return Section(
        cv_section_header("Skills"),
        Grid(
            *[
                Div(
                    H3(
                        cat.upper(),
                        style="font-weight: 700; font-size: 0.875rem; color: var(--color-white); margin-bottom: 1rem; border-bottom: 1px solid var(--color-base-900); padding-bottom: 0.5rem;",
                    ),
                    Ul(
                        *[
                            Li(
                                s,
                                style="color: var(--color-base-400); font-size: 0.875rem; margin-bottom: 0.5rem;",
                            )
                            for s in items
                        ],
                        style="list-style-type: none; padding-left: 0;",
                    ),
                    style="padding: 1.5rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary);",
                )
                for cat, items in skills.items()
            ],
            cols_min=1,
            cols_md=3,
            cls="gap-8",
        ),
    )


def cv_patents():
    patents = [
        {
            "title": "Extract, consumable product and method for enriching bioactive metabolite in an extract",
            "authors": "Chae, L. H., Flatt, J., Herrmann, A. M., Navarro, G., Ochoa, J. L.",
            "link": "https://patents.google.com/patent/US11647776B2/en",
            "year": "2023",
        },
        {
            "title": "Methods for making and using novel semi-synthetic small molecules for the treatment parasitic disease",
            "authors": "Roger R Linington, Gabriel Navarro, Khanitha Pudhom, James McKerrow",
            "link": "https://patents.google.com/patent/US9290474B2/en",
            "year": "2016",
        },
        {
            "title": "Semi-synthetic small molecules for the treatment parasitic disease",
            "authors": "Roger Linington, Gabriel Navarro, Khanitha Pudhom, James McKerrow",
            "link": "https://patents.google.com/patent/US8946455B2/en",
            "year": "2015",
        },
        {
            "title": "Novel semi-synthetic small molecules for the treatment parasitic disease",
            "authors": "Khanitha Pudhom, Gabriel Navarro, James McKerrow, Roger Linington",
            "link": "https://patents.google.com/patent/US20140236030A1/en",
            "year": "2014",
        },
    ]
    return Section(
        cv_section_header("Patents"),
        Grid(
            *[
                Div(
                    P(
                        p["year"],
                        style="font-weight: 700; color: var(--color-base-500); font-size: 0.875rem; margin-bottom: 0.5rem;",
                    ),
                    H3(
                        p["title"].upper(),
                        style="margin-top: 0; color: var(--color-white); font-weight: 700; font-size: 1rem; line-height: 1.4;",
                    ),
                    P(
                        p["authors"],
                        style="color: var(--color-base-400); font-size: 0.75rem; margin-bottom: 1rem;",
                    ),
                    A(
                        "VIEW PATENT →",
                        href=p["link"],
                        style="color: var(--color-accent-100); font-weight: 700; font-size: 0.75rem; text-decoration: none; letter-spacing: 0.05em;",
                    ),
                    style="padding: 1.5rem; border: 1px solid var(--color-base-900); border-radius: var(--radius-lg); background: var(--dark-base-secondary);",
                )
                for p in patents
            ],
            cols_min=1,
            cols_md=2,
            cls="gap-8",
        ),
    )


def cv_publications():
    pubs = [
        {
            "title": "Tau oligomers modulate synapse fate by eliciting progressive bipartite synapse dysregulation and synapse loss",
            "authors": "Pareja-Navarro, K. A., King, C. D., Kauwe, G., Ngwala, Y. Y., Lokitiyakul, D., Wong, I., Vira, A., Chen, J. H., Sharma, M., Navarro, G.",
            "info": "bioRxiv (Under Review: Molecular Neurodegeneration), 2026",
        },
        {
            "title": "Portobelamides A and B and caciqueamide, cytotoxic peptidic natural products from a Caldora sp. marine cyanobacterium",
            "authors": "Demirkiran, O., Almaliti, J., Leao, T., Navarro, G., Byrum, T., Valeriote, F. A., Gerwick, L., Gerwick, W. H.",
            "info": "Journal of Natural Products, 84(8), 2081-2093, 2021",
        },
        {
            "title": "Evaluating nitrogen-containing biosynthetic products produced by saltwater culturing of several California littoral zone Gram-negative bacteria",
            "authors": "Lorig-Roach, N., Still, P. C., Coppage, D., Compton, J. E., Crews, M. S., Navarro, G., Tenney, K., Crews, P.",
            "info": "Journal of Natural Products, 80(8), 2304-2310, 2017",
        },
        {
            "title": "Biofilm formation and detachment in Gram-negative pathogens is modulated by select bile acids",
            "authors": "Sanchez, L. M., Cheng, A. T., Warner, C. J. A., Townsley, L., Peach, K. C., Navarro, G., Shikuma, N. J., Bray, W. M., Riener, R. M., Yildiz, F. H.",
            "info": "PLoS One, 11(3), e0149603, 2016",
        },
        {
            "title": "Kalkipyrone B, a marine cyanobacterial γ-pyrone possessing cytotoxic and anti-fungal activities",
            "authors": "Bertin, M. J., Demirkiran, O., Navarro, G., Moss, N. A., Lee, J., Goldgof, G. M., Vigil, E., Winzeler, E. A., Valeriote, F. A., Gerwick, W. H.",
            "info": "Phytochemistry, 122, 113-118, 2016",
        },
        {
            "title": "Salinipostins A–K, long-chain bicyclic phosphotriesters as a potent and selective antimalarial chemotype",
            "authors": "Navarro, G., Schulze, C. J., Ebert, D., DeRisi, J., Linington, R. G.",
            "info": "The Journal of Organic Chemistry, 80(3), 1312-1320, 2015",
        },
        {
            "title": "Abyssomicin 2 reactivates latent HIV-1 by a PKC- and HDAC-independent mechanism",
            "authors": "Navarro, G., León, B., Dickey, B. J., Stepan, G., Tsai, A., Jones, G. S., Morales, M. E., Barnes, T., Ahmadyar, S., Tsiang, M.",
            "info": "Organic Letters, 17(2), 262-265, 2015",
        },
        {
            "title": "Isolation of polycavernoside D from a marine cyanobacterium",
            "authors": "Navarro, G., Cummings, M. E., Lee, J., Moss, N., Glukhov, E., Valeriote, F. A., Gerwick, L., Gerwick, W. H.",
            "info": "Environmental Science & Technology Letters, 2(7), 166-170, 2015",
        },
        {
            "title": "Mass spectrometry tools for screening of marine cyanobacterial natural products",
            "authors": "Knaan, T. L., Garg, N., Peng, Y., Alexandrov, T., Navarro, G., Glukhov, E., Gerwick, L., Gerwick, W. H., Dorrestein, P. C.",
            "info": "Planta Medica, 81(11), PQ6, 2015",
        },
        {
            "title": "Honaucin A, mechanism of action and role as a potential cancer prevention agent",
            "authors": "Gerwick, L., Mascuch, S. J., Navarro, G., Boudreau, P., Carland, T. M., Gaasterland, T., Gerwick, W. H.",
            "info": "Planta Medica, 81(11), PW2, 2015",
        },
        {
            "title": "Image-based 384-well high-throughput screening method for the discovery of skyllamycins A to C as biofilm inhibitors and inducers of biofilm detachment in Pseudomonas aeruginosa",
            "authors": "Navarro, G., Cheng, A. T., Peach, K. C., Bray, W. M., Bernan, V. S., Yildiz, F. H., Linington, R. G.",
            "info": "Antimicrobial Agents and Chemotherapy, 58(2), 1092-1099, 2014",
        },
        {
            "title": "Hit-to-lead development of the chamigrane endoperoxide merulin A for the treatment of African sleeping sickness",
            "authors": "Navarro, G., Chokpaiboon, S., De Muylder, G., Bray, W. M., Nisam, S. C., McKerrow, J. H., Pudhom, K., Linington, R. G.",
            "info": "PLoS Neglected Tropical Diseases (or similar), 2012",
        },
        {
            "title": "An image-based 384-well high-throughput screening method for phenotypic discovery of biofilm inhibitors in Pseudomonas aeruginosa",
            "authors": "Navarro, G., Peach, K. C., Cheng, A., Bray, W. M., Yildiz, F. H., Linington, R. G.",
            "info": "Planta Medica, 78(11), PD145, 2012",
        },
        {
            "title": "Versatile Method for the Detection of Covalently Bound Substrates on Solid Supports by DART Mass Spectrometry",
            "authors": "Sanchez, L. M., Curtis, M. E., Bracamonte, B. E., Kurita, K. L., Navarro, G., Sparkman, O. D., Linington, R. G.",
            "info": "Organic Letters, 2011",
        },
        {
            "title": "Highlights of marine invertebrate-derived biosynthetic products: Their biomedical potential and possible production by microbial associants",
            "authors": "Radjasa, O. K., Vaske, Y. M., Navarro, G., Vervoort, H. C., Tenney, K., Linington, R. G., Crews, P.",
            "info": "Bioorganic & Medicinal Chemistry, 2011",
        },
        {
            "title": "Biomimetic synthesis of the shimalactones",
            "authors": "Sofiyev, V., Navarro, G., Trauner, D.",
            "info": "Organic Letters, 10(1), 149-152, 2008",
        },
    ]
    return Section(
        cv_section_header("Publications"),
        Grid(
            *[
                Div(
                    H3(
                        p["title"].upper(),
                        style="margin-top: 0; color: var(--color-white); font-weight: 700; font-size: 1rem; line-height: 1.4;",
                    ),
                    P(
                        p["authors"],
                        style="color: var(--color-base-400); font-size: 0.875rem; margin-bottom: 0.5rem;",
                    ),
                    P(
                        p["info"],
                        style="color: var(--color-accent-100); font-weight: 700; font-size: 0.75rem;",
                    ),
                    style="padding: 1.5rem; border-bottom: 1px solid var(--color-base-900);",
                )
                for p in pubs
            ],
            cols_min=1,
            cols_md=1,
            cls="gap-4",
        ),
    )
