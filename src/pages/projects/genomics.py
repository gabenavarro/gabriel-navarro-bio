from fasthtml.common import (
    Titled,
    Style,
    Div,
    A,
    H1,
    Span,
    P,
    Script,
    Header,
    Section,
    H2,
    Img,
    Ul,
    Li,
    H3,
    Article,
    Grid,
    Footer
)

GENOMICS_PROJECT = Titled("Large-Scale Genomics Pipeline",
        Div(
            # Header section with key title and brief intro
            Header(
                H1("Large-Scale Genomics Pipeline", cls="title"),
                P("A petabyte-scale genomics data processing solution on Google Cloud Platform", cls="subtitle"),
                cls="header-container"
            ),
            
            # Skills section
            Section(
                H2("Technical Skills Showcased"),
                Div(
                    Span("Bioinformatician", cls="skill-tag"),
                    Span("Data Engineer", cls="skill-tag"),
                    Span("Cloud Architect", cls="skill-tag"),
                    Span("Genomics Expert", cls="skill-tag"),
                    Span("Python Developer", cls="skill-tag"),
                    Span("Problem Solver", cls="skill-tag"),
                    Span("Cross-Functional Expert", cls="skill-tag"),
                    cls="skills-container"
                ),
                cls="section"
            ),
            
            # Project overview section
            Section(
                H2("Project Overview"),
                P("Developed and deployed a comprehensive genomics pipeline capable of handling petabyte-scale sequencing data from major public repositories including NCBI and EBI. The solution provides end-to-end processing from raw sequencing reads to actionable biological insights."),
                Img(src="/api/placeholder/800/400", alt="Genomics Pipeline Architecture Diagram", cls="overview-image"),
                cls="section"
            ),
            
            # Key achievements section
            Section(
                H2("Key Achievements"),
                Ul(
                    Li(
                        H3("Microservice Architecture"),
                        P("Designed and implemented a containerized microservice architecture using Docker, enabling modular, maintainable, and scalable deployments across the entire genomics analysis workflow.")
                    ),
                    Li(
                        H3("Cloud-Native Computing"),
                        P("Leveraged GCP Batch and Google Cloud Run for massively parallel processing, achieving 20-50x speedup compared to traditional sequential processing methods while maintaining cost efficiency.")
                    ),
                    Li(
                        H3("Data Science Integration"),
                        P("Applied Python's scientific stack (NumPy, Pandas, Biopython) to extract genomic features, perform quality control checks, and prepare data for downstream analysis and machine learning applications.")
                    ),
                    Li(
                        H3("Cross-Functional Collaboration"),
                        P("Led collaboration between biologists, computational scientists, and machine learning specialists, developing shared APIs and data models that bridged domain knowledge gaps.")
                    ),
                    cls="achievements-list"
                ),
                cls="section"
            ),
            
            # Technical details section
            Section(
                H2("Technical Implementation"),
                Article(
                    H3("Pipeline Components"),
                    Ul(
                        Li("Data Ingestion: Custom adapters for NCBI SRA, EBI ENA, and private sequencing repositories"),
                        Li("Quality Control: FastQC integration with custom filtering pipelines"),
                        Li("Read Alignment: BWA-MEM and HISAT2 containerized modules"),
                        Li("Variant Calling: GATK4 and FreeBayes parallel processing"),
                        Li("Feature Extraction: Custom Python modules for genomic feature analysis"),
                        Li("Visualization: Interactive dashboards using Plotly and custom web interfaces")
                    )
                ),
                Article(
                    H3("Cloud Infrastructure"),
                    Ul(
                        Li("Storage: GCP Cloud Storage with lifecycle policies for cost optimization"),
                        Li("Compute: Batch processing using GCP Batch and Dataproc"),
                        Li("Orchestration: Workflow management with Nextflow and Cloud Composer"),
                        Li("Monitoring: Custom alerting system integrated with Cloud Monitoring"),
                        Li("Security: VPC Service Controls with fine-grained IAM policies")
                    )
                ),
                Article(
                    H3("Data Scale"),
                    Ul(
                        Li("Raw Data: 2.5+ petabytes of sequencing data"),
                        Li("Processed Results: 500+ terabytes of analysis results"),
                        Li("Database: 50+ billion genomic variants indexed for rapid query"),
                        Li("Computing: Peak capacity of 100,000+ vCPUs during large processing runs")
                    )
                ),
                cls="section technical-details"
            ),
            
            # Results section
            Section(
                H2("Impact & Results"),
                Article(
                    P("The genomics pipeline has enabled researchers to process and analyze sequencing data at unprecedented scale and speed:"),
                    Ul(
                        Li("Reduced processing time from weeks to hours for typical genome datasets"),
                        Li("Enabled analysis of 50,000+ whole genomes in a single coordinated run"),
                        Li("Decreased computing costs by 65% through optimized resource allocation"),
                        Li("Facilitated discovery of novel genetic variants associated with rare diseases"),
                        Li("Supported multiple research publications in high-impact journals")
                    )
                ),
                cls="section"
            ),
            
            # Technologies list section
            Section(
                H2("Technologies Used"),
                Grid(
                    Div(
                        H3("Cloud & Infrastructure"),
                        Ul(
                            Li("Google Cloud Platform (GCP)"),
                            Li("Docker & Container Registry"),
                            Li("Kubernetes / GKE"),
                            Li("Terraform / Cloud Deployment Manager"),
                            Li("Cloud Storage / Cloud SQL")
                        ),
                        cls="tech-column"
                    ),
                    Div(
                        H3("Genomics Tools"),
                        Ul(
                            Li("BWA-MEM / HISAT2"),
                            Li("GATK4 / FreeBayes"),
                            Li("Samtools / BCFtools"),
                            Li("Picard Tools"),
                            Li("PLINK / EIGENSTRAT")
                        ),
                        cls="tech-column"
                    ),
                    Div(
                        H3("Programming & Data"),
                        Ul(
                            Li("Python (NumPy, Pandas, Biopython)"),
                            Li("R (Bioconductor, ggplot2)"),
                            Li("SQL / BigQuery"),
                            Li("Nextflow / WDL"),
                            Li("Bash / awk / sed")
                        ),
                        cls="tech-column"
                    ),
                    cls="technologies-grid"
                ),
                cls="section"
            ),
            
            # Footer section
            Footer(
                P("© 2025 All Rights Reserved"),
                P(A("Contact for more information", href="#"), cls="contact-link"),
                cls="footer"
            ),
            
            cls="container"
        ),
        Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
        Style("""
            :root {
                --primary-color: #023047;
                --secondary-color: #219ebc;
                --accent-color: #ffb703;
                --light-bg: #f8f9fa;
                --text-color: #333;
                --light-text: #666;
                --header-font: system-ui, 'Inter', sans-serif;
                --body-font: system-ui, 'Inter', sans-serif;
            }
            
            body {
                font-family: var(--body-font);
                color: var(--text-color);
                line-height: 1.7;
                margin: 0;
                background-color: var(--light-bg);
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem 1rem;
            }
            
            .header-container {
                text-align: center;
                padding: 3rem 1rem;
                margin-bottom: 2rem;
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                color: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            
            .title {
                font-size: 2.8rem;
                margin-bottom: 1rem;
                font-weight: 700;
                font-family: var(--header-font);
            }
            
            .subtitle {
                font-size: 1.4rem;
                max-width: 700px;
                margin: 0 auto;
                font-weight: 300;
            }
            
            .section {
                margin: 3rem 0;
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }
            
            .section h2 {
                color: var(--primary-color);
                border-bottom: 2px solid var(--accent-color);
                padding-bottom: 0.5rem;
                margin-bottom: 1.5rem;
                font-family: var(--header-font);
            }
            
            .skills-container {
                display: flex;
                flex-wrap: wrap;
                gap: 0.8rem;
                margin-top: 1rem;
            }
            
            .skill-tag {
                background-color: var(--primary-color);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 50px;
                font-size: 0.9rem;
                display: inline-block;
            }
            
            .overview-image {
                width: 100%;
                border-radius: 4px;
                margin: 1.5rem 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            .achievements-list li {
                margin-bottom: 1.5rem;
                padding-bottom: 1.5rem;
                border-bottom: 1px solid #eee;
            }
            
            .achievements-list li:last-child {
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }
            
            .achievements-list h3 {
                color: var(--secondary-color);
                margin-bottom: 0.5rem;
                font-family: var(--header-font);
            }
            
            .technical-details article {
                margin-bottom: 2rem;
            }
            
            .technical-details h3 {
                color: var(--secondary-color);
                margin-bottom: 1rem;
                font-family: var(--header-font);
            }
            
            .technologies-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
            }
            
            .tech-column h3 {
                color: var(--secondary-color);
                margin-bottom: 1rem;
                font-family: var(--header-font);
            }
            
            .tech-column ul {
                padding-left: 1.5rem;
            }
            
            .tech-column li {
                margin-bottom: 0.5rem;
            }
            
            .footer {
                text-align: center;
                padding: 2rem 0;
                margin-top: 3rem;
                color: var(--light-text);
                border-top: 1px solid #eee;
            }
            
            .contact-link {
                color: var(--secondary-color);
                text-decoration: none;
                font-weight: 500;
            }
            
            .contact-link:hover {
                text-decoration: underline;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .title {
                    font-size: 2.2rem;
                }
                
                .subtitle {
                    font-size: 1.1rem;
                }
                
                .technologies-grid {
                    grid-template-columns: 1fr;
                }
                
                .section {
                    padding: 1.5rem;
                }
            }
        """)
    )