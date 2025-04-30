from fasthtml.common import Div, A, H2, P, Ul, Li, Section, H3


CV_CSS = """

/* Main Content Styles */
.section {
    padding: var(--section-spacing) 0;
    scroll-margin-top: 4rem;
    margin-bottom: 18rem;
}

.section-title {
    font-size: 2rem;
    position: relative;
    padding-bottom: 0.5rem;
}


/* Contact Info */
.contact-info {
    margin-bottom: 2rem;
    font-size: 1.1rem;
}

.contact-info p {
    margin-bottom: 0.5rem;
}

.contact-info a {
    color: var(--secondary-color);
    text-decoration: none;
}

.contact-info a:hover {
    text-decoration: underline;
}

/* Summary */
.summary {
    background-color: var(--dark-newspaper-bg);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 3rem;
    border-left: 4px solid var(--secondary-color);
}

/* Experience */
.experience-item {
    margin-bottom: 3rem;
    position: relative;
}

.experience-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.experience-company {
    font-size: 1.2rem;
    color: var(--secondary-color);
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.experience-period {
    font-size: 1rem;
    color: var(--text-color-secondary);
    margin-bottom: 1rem;
    font-style: italic;
}

.experience-description ul {
    list-style-position: inside;
    margin-left: 1rem;
}

.experience-description li {
    margin-bottom: 0.5rem;
}

/* Skills */
.skills-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.skill-category {
    background-color: var(--dark-newspaper-bg);
    padding: 1.5rem;
    border-radius: 10px;
}

.skill-category h3 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--secondary-color);
}

.skill-list {
    list-style: none;
}

.skill-list li {
    margin-bottom: 0.5rem;
    position: relative;
    padding-left: 1.5rem;
}

.skill-list li::before {
    content: '•';
    position: absolute;
    left: 0;
    color: var(--secondary-color);
    font-weight: bold;
}

/* Education */
.education-item {
    margin-bottom: 2rem;
}

.education-degree {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.education-institution {
    font-size: 1.1rem;
    color: var(--secondary-color);
    margin-bottom: 0.5rem;
}

.education-period {
    font-size: 1rem;
    color: var(--text-color-secondary);
    font-style: italic;
}

/* Patents & Publications */
.patent-item, .publication-item {
    margin-bottom: 1.5rem;
    padding-left: 1rem;
    border-left: 2px solid var(--secondary-color);
}

.patent-title, .publication-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.patent-authors, .publication-authors {
    font-size: 1rem;
    color: var(--text-color-secondary);
    margin-bottom: 0.5rem;
}

.patent-link, .publication-link {
    font-size: 0.9rem;
    color: var(--secondary-color);
    word-break: break-word;
}

.patent-year, .publication-year {
    font-size: 0.9rem;
    color: var(--text-color-secondary);
    margin-top: 0.5rem;
}

/* Footer */
footer {
    background-color: rgba(0, 0, 0, 0.3);
    padding: 2rem 0;
    text-align: center;
    margin-top: 4rem;
}

.footer-text {
    color: var(--text-color-secondary);
    font-size: 0.9rem;
}

/* Responsive Styles */
@media (max-width: 768px) {
    .section-title {
        font-size: 2rem;
    }
    
    .skills-container {
        grid-template-columns: 1fr;
    }
}
"""


def cv_contact():
    """ Create a contact section for the CV page. """
    return Div(
        # Contact Information
        Section(
            H2("Contact Information", cls="section-title"),
            Div(
                P("📍 Moraga, CA"),
                P("✉️ ", A("gchinonavarro@gmail.com", href="mailto:gchinonavarro@gmail.com")),
                P("🌐 ", A("https://gabriel.navarro.bio", href="https://gabriel.navarro.bio", target="_blank")),
            ),
            cls="section",
        )
    )

def cv_summary():
    """ Create a summary section for the CV page. """
    return Div(
        # Summary
        Section(
            H2("Summary", cls="section-title"),
            Div(
                P("Computational Scientist with 10+ years' expertise in omics ML modeling. Proven track record of designing and deploying AI/ML-powered bioinformatics pipelines, assessing biological application, and developing high-throughput omics data solutions on cloud platforms. Adept at collaborating with cross-functional teams to deliver robust, efficient solutions that drive critical insights in life sciences."),
            ),
            cls="section",
        ),
        cls="section",
    )

def cv_experience():
    """ Create an experience section for the CV page. """
    return Section(
        H2("Work Experience", cls="section-title"),
        # Experience Item 1
        Div(
            H3("Senior Bioinformatics Scientist, Computational Scientist", cls="experience-title"),
            P("Triplebar", cls="experience-company"),
            P("January 2024 — Present", cls="experience-period"),
            Div(
                Ul(
                    Li("Developed custom AI/ML models for synthetic biology applications, fine-tuning pLMs to analyze antibody datasets that improved prediction accuracy by 42% and reduced experimental validation, accelerating discovery timelines."),
                    Li("Architected GCP bioinformatics infrastructure that cut processing time by 65% and increased throughput 10x, enabling 200+ weekly genomic analysis."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),
        
        # Experience Item 2
        Div(
            H3("Data Scientist III, Computational Scientist", cls="experience-title"),
            P("Amyris", cls="experience-company"),
            P("December 2021 — December 2023", cls="experience-period"),
            Div(
                Ul(
                    Li("Deployed multi-omics platform reducing analysis time by 75%, enabling 3x higher monthly strain design evaluation."),
                    Li("Created Python/Dash visualization dashboards that drove 75% increase in self-service analytics adoption across R&D teams."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),

        # Experience Item 3
        Div(
            H3("Senior Scientist, Computational Metabolomics", cls="experience-title"),
            P("Hexagon Bio", cls="experience-company"),
            P("March 2020 — November 2021", cls="experience-period"),
            Div(
                Ul(
                    Li("Built high-throughput metabolomics pipeline processing 4+ TB of LC-MS/MS data with 85% recall in compound identification and <5% false discovery rate."),
                    Li("Designed and implemented machine learning algorithms that successfully identified 16 novel fungal compound classes with demonstrated biological activity."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),

        # Experience Item 4
        Div(
            H3("Lead Scientist, Computational Metabolomics", cls="experience-title"),
            P("Brightseed", cls="experience-company"),
            P("February 2018 — February 2020", cls="experience-period"),
            Div(
                Ul(
                    Li("Developed core metabolomics technology platform for Forager™, Brightseed's proprietary AI system, resulting in a 1000x increase in phytonutrient identification throughput."),
                    Li("Created ML algorithms mapping 20,000+ plant compounds to human health benefits, establishing first-of-its-kind bioactive database."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),

        # Experience Item 5
        Div(
            H3("Consultant", cls="experience-title"),
            P("Mondelez", cls="experience-company"),
            P("February 2018 — July 2019", cls="experience-period"),
            Div(
                Ul(
                    Li("Provided strategic expertise to develop and optimize 12 mass spectrometry-based metabolomics protocols that improved compound detection sensitivity."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),

        # Experience Item 6
        Div(
            H3("Senior Scientist, Mass Spectrometry", cls="experience-title"),
            P("Mondelez", cls="experience-company"),
            P("January 2016 — January 2018", cls="experience-period"),
            Div(
                Ul(
                    Li("Pioneered machine learning-based algorithms for mass spectrometry data that reduced analysis time by 90%, enabling rapid quality control decisions for food product development across 3 global manufacturing facilities."),
                ),
                cls="experience-description"
            ),
            cls="experience-item"
        ),
        cls="section",
    )


def cv_skills():
    """ Create a skills section for the CV page. """

    return Section(
        H2("Skills", cls="section-title"),
        # Skills            
        Div(
            Div(
                H3("Machine Learning & AI"),
                Ul(
                    Li("Genomic and protein language model training and fine-tuning"),
                    Li("Embedding space analysis"),                    
                ), 
                cls="skill-category"
            ),
            Div(
                H3("Computational Skills"),
                Ul(
                    Li("Python, Bash scripting"),
                    Li("PyTorch, ESMFold, AlphaFold"),
                    Li("Scikit-learn, RDKit"),
                    Li("Dash, VertexAI, Kubeflow"),
                    Li("Docker, WSL"),
                ), cls="skill-category"
            ),
            Div(
                H3("Computational Biology & Genomics"),
                Ul(
                    Li("NGS Data"),
                    Li("Mass spectrometry-based metabolomics and proteomic"),
                    Li("High-throughput sequencing analysis"),
                ), cls="skill-category"
                
            ),
            Div(
                H3("Cloud & Data Infrastructure"),
                Ul(
                    Li("GCP (Batch Computing, Vertex AI)"),
                    Li("Docker"),
                    Li("Cloud-Native Systems"),
                ), cls="skill-category"
            ),
            cls="skills-container",
        ),
        cls="section"
    )


def cv_education():
    """ Create an education section for the CV page. """
    return Section(
        H2("Education", cls="section-title"),
        Div(
            # Education Item 1
            Div(
                H3("Postdoctoral Researcher, IRACDA Fellow", cls="education-degree"),
                P("University of California, San Diego", cls="education-institution"),
                P("2014 — 2015", cls="education-period"),
            ),
            
            # Education Item 2
            Div(
                H3("PhD in Chemistry, NSF GRFP Fellow", cls="education-degree"),
                P("University of California Santa Cruz", cls="education-institution"),
                P("2008 — 2013", cls="education-period"),
            ),
            
            # Education Item 3
            Div(
                H3("Bachelor of Science in Chemical Biology", cls="education-degree"),
                P("University of California Berkeley", cls="education-institution"),
                P("2004 — 2008", cls="education-period"),
            ),
        ),
        cls="section",
    )


def cv_patents():
    """ Create a patents section for the CV page. """
    return Section(
        H2("Patents", cls="section-title"),
        Div(
            # Patent Item 1
            Div(
                H3("Methods for making and using novel semi-synthetic small molecules for the treatment parasitic disease", cls="patent-title"),
                P("Roger Linington, Gabriel Navarro, Khanitha Pudhom, James McKerrow", cls="patent-authors"),
                A("https://patents.google.com/patent/US9290474B2/en", href="https://patents.google.com/patent/US9290474B2/en", target="_blank", cls="patent-link"),
                P("2016", cls="patent-year"),
            ),
            
            # Patent Item 2
            Div(
                H3("Semi-Synthetic Small Molecules for the Treatment Parasitic Disease", cls="patent-title"),
                P("Roger R Linington, Gabriel Navarro, Khanitha Pudhom, James McKerrow", cls="patent-authors"),
                A("https://patents.google.com/patent/US8946455B2/en", href="https://patents.google.com/patent/US8946455B2/en", target="_blank", cls="patent-link"),
                P("2015", cls="patent-year"),
            ),
        ),
        cls="section",
    )


def cv_publications():
    """ Create a publications section for the CV page. """
    return Section(
        H2("Publications", cls="section-title"),
        Div(
            # Publication Item 1
            Div(
                H3("Biofilm Formation and Detachment in Gram-Negative Pathogens Is Modulated by Select Bile Acids", cls="publication-title"),
                P("Laura M. Sanchez, Andrew Cheng, Christopher J.A. Warner, Loni Townsley, Kelly C. Peach, Gabriel Navarro, Nicholas J. Shikuma, Walter M. Bray, Romina M. Riener, Fitnat H. Yildiz, Roger G. Linington", cls="publication-authors"),
                P("PLoS One, 2016, 11, e0149603", cls="publication-link"),
            ),
            
            # Publication Item 2
            Div(
                H3("Kalkipyrone B, a Marine Cyanobacterial γ-Pyrone Possessing Cytotoxic and Anti-Fungal Activities", cls="publication-title"),
                P("Matthew J. Bertin, Ozlem Demirkiran, Gabriel Navarro, Nathan A. Moss, John Lee, Gregory M. Goldgof, Edgar Vigil, Elizabeth A Winzeler, Fred A Valeriote, William H. Gerwick", cls="publication-authors"),
                P("Phytochemistry, 2016, 122, 113-118", cls="publication-link"),
            ),
            
            # Publication Item 3
            Div(
                H3("Isolation of Polycavernoside D from a Marine Cyanobacterium", cls="publication-title"),
                P("Gabriel Navarro, Susie Cummings, John Lee, Nathan Moss, Evgenia Glukhov, Fred A. Valeriote, Lena Gerwick, William H. Gerwick", cls="publication-authors"),
                P("Environmental Science & Technology Letters, 2015, 2, 166-170", cls="publication-link"),
            ),
            
            # Publication Item 4
            Div(
                H3("Salinipostins A—K, Long-Chain Bicyclic Phosphotriesters as a Potent and Selective Antimalarial Chemotype", cls="publication-title"),
                P("Christopher J. Schulze*, Gabriel Navarro*, Daniel Ebert, Joseph L. DeRisi, Roger G. Linington (* Co-ﬁrst author)", cls="publication-authors"),
                P("The Journal of Organic Chemistry. 2015, 80, 1312", cls="publication-link"),
                P("1320", cls="publication-link"),
            ),
            # Publication Item 5
            Div(
                H3("Abyssomicin 2 Reactivates Latent HIV-1 by a PKC-and HDAC-Independent Mechanism", cls="publication-title"),
                P("Brian Leon*, Gabriel Navarro*, Bailey J. Dickey, George Stepan, Angela Tsai, Gregg S. Jones, Monica E. Morales, Tiffany Barnes, Shekeba Ahmadyar, Manuel Tsiang, Romas Geleziunas, Tomas Cihlar, Nikos Pagratis, Yang Tian, Helen Yu, Roger G. Linington (* Co-ﬁrst author)", cls="publication-authors"),
                P("Organic Letters. 2015, 17, 262-265", cls="publication-link"),
            ),
            # Publication Item 6
            Div(
                H3("Image-based 384-well high-throughput screening method for the discovery of skyllamycins A to C as biofilm inhibitors and inducers of biofilm detachment in Pseudomonas aeruginosa", cls="publication-title"),
                P("Gabriel Navarro, Andrew Cheng, Kelly C. Peach, Walter M. Bray, Valerie S. Bernan, Fitnat H. Yildiz, Roger G. Linington", cls="publication-authors"),
                P("Antimicrobial Agents and Chemotherapy. 2014¸58, 1092-1099", cls="publication-link"),
            ),
            # Publication Item 7
            Div(
                H3("Hit-to-Lead Development of the Chamigrane Endoperoxide Merulin A for the Treatment of African Sleeping Sickness", cls="publication-title"),
                P("Gabriel Navarro, Supchar Chokpaiboon, Geraldine DeMuylder, Walter M. Bray, Sean C. Nisam, James H. McKerrow, Khanitha Pudhom, Roger G. Linington", cls="publication-authors"),
                P("PLoS ONE, 2012, 7, e46172", cls="publication-link"),
            ),
            # Publication Item 8
            Div(
                H3("Highlights of Marine Invertebrate-Derived Biosynthetic Products: Their Biomedical Potential and Possible Production by Microbial Associates", cls="publication-title"),
                P("Gabriel Navarro, Roger G. Linington", cls="publication-authors"),
                P("Marine Drugs, 2012, 10, 383-420", cls="publication-link"),
            ),
        

            # Publication Item 9
            Div(
                H3("Versatile Method for the Detection of Covalently Bound Substrates on Solid Supports by DART Mass Spectrometry", cls="publication-title"),
                P("Laura M. Sanchez, Matthew E. Curtis, Bianca E. Bracamonte, Kenji L. Kurita, Gabriel Navarro, David O. Sparkman, Roger G. Linington", cls="publication-authors"),
                P("Organic Letters, 2011, 13, 3770-3773", cls="publication-link"),
            ),
            # Publication Item 10
            Div(
                H3("Biomimetic Synthesis of the Shimalactones", cls="publication-title"),
                P("Vladimir Sofiyev, Gabriel Navarro, Dirk Trauner", cls="publication-authors"),
                P("Organic Letters, 2008, 10, 149-152", cls="publication-link"),
            ),
        ),
        cls="section",
    )