from fasthtml.common import Style, Div, Script, Img, H1, H3, P
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MasonryJS, MarkedJS
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

def image_card(i):
    return Div(
        Img(
            src=f"https://picsum.photos/id/{i + 100}/600/{rando.randint(a=200,b=500)}", 
            alt=f"Image {i}",
            cls="rounded-img",
        ),
        H3(f"Image Title {i}", cls="white"),
        P(f"This is a description for image {i}", cls="white"),
        cls="masonry-card masonry-sizer"
    )


# TODO: Move this to bigquery for blog posts and for cards
def marked_section():
    return Div(
        """
# Mastering Quality Control in Omics with FastQC

Quality control (QC) of sequencing data is a foundational step in bioinformatics workflows, crucial for ensuring reliable and accurate results in omics analyses. Among the many available tools, **FastQC** has emerged as an industry-standard software for performing quality assessments of FASTQ files.

## What is FastQC?

[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) is a widely-used quality control tool designed specifically for high-throughput sequencing data. It provides rapid analysis and visualization of sequencing reads, highlighting potential issues like poor sequencing quality, adapter contamination, and biases in the sequencing library.

## Key Features of FastQC

FastQC evaluates multiple quality metrics and provides intuitive graphical reports:

- **Basic Statistics**: Read counts, sequence length, and GC content.
- **Per-base Sequence Quality**: Quality scores across read length.
- **Per-sequence Quality Scores**: Distribution of average read quality scores.
- **Per-base Sequence Content**: Detects biases in base composition.
- **Per-sequence GC Content**: Checks for unexpected GC-content distributions.
- **Adapter Content**: Identifies the presence and level of adapter contamination.
- **Sequence Duplication Levels**: Highlights redundant reads.
- **Overrepresented Sequences**: Finds sequences occurring more frequently than expected.

## Why Choose FastQC?

### User-Friendly Interface
FastQC is simple to run and interpret. Its HTML reports include clear visuals, making data assessment straightforward even for beginners.

### Comprehensive QC Reports
With detailed graphical and statistical outputs, FastQC provides immediate insights into the quality and reliability of sequencing data, allowing for quick troubleshooting.

### Integration with Workflow Managers
FastQC integrates seamlessly with popular workflow management tools like Snakemake, Nextflow, and Galaxy, streamlining high-throughput data analysis pipelines.

## Getting Started with FastQC

### Installation
FastQC is straightforward to install:

```bash
# Using Conda
conda install -c bioconda fastqc

# Alternatively, directly download from the FastQC website
wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
unzip fastqc_v0.12.1.zip
chmod +x FastQC/fastqc
```

### Basic Usage Example

Running FastQC on single-end reads:

```bash
fastqc sample.fastq -o output_directory
```

- `sample.fastq`: The FASTQ file to be assessed.
- `-o`: Specifies the directory for output reports.

For paired-end data:

```bash
fastqc sample_R1.fastq sample_R2.fastq -o output_directory
```

## Interpreting FastQC Reports

FastQC reports use traffic-light indicators:

- 🟢 **Pass**: The metric falls within an acceptable range.
- 🟡 **Warn**: Potential issues; requires careful interpretation.
- 🔴 **Fail**: Significant quality issues that require intervention.

Common issues identified by FastQC:
- **Quality Drop-off at Read Ends**: Indicates the need for trimming.
- **Adapter Contamination**: Indicates incomplete adapter removal during sequencing.
- **Sequence Duplication**: Suggests PCR bias or library complexity issues.

## Integrating FastQC into Your Workflow

FastQC is ideally used in conjunction with preprocessing tools like fastp or Trimmomatic. Typically, you would:

1. Run FastQC to assess initial data quality.
2. Preprocess (e.g., adapter trimming, quality filtering).
3. Re-run FastQC to confirm data improvements.

## Conclusion

FastQC remains indispensable in modern bioinformatics, providing clear, actionable insights into sequencing data quality. Integrating FastQC into your omics workflows helps ensure robust and reliable data analysis outcomes.

Happy sequencing and quality checking!

---

**References:**

- [FastQC Documentation](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
        """,
        cls="marked"
    )


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
        marked_section(),
        Div(
            Div(
                *[image_card(i) for i in range(1, 20) if i != 5],
                cls="masonry-container",
            ),
        ),
        cls="container",
        
    )



MASONRY_PAGE = create_blog_page()