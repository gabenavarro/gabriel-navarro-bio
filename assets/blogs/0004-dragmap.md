@{id = "a10b19fa-8736-485e-b8b7-a0f0bd5ce22d"
  title = "Dragen-GATK: High-Performance Variant Calling"
  date = "2025-04-26T00:00:00Z"
  tags = ['docker', 'bioinformatics', 'genomics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/gatk-dragen-thumb.svg"
  description = "Dragen-GATK combines Illumina’s hardware acceleration with GATK’s best-practice workflows to deliver ultra-fast, clinically robust germline variant calling. This guide walks you through Docker-based setup, sample analysis, and key parameters to optimize high-performance variant discovery in genomics projects."
  type = "note"
  disabled = false
}
# High-Performance Variant Calling with Dragen-GATK

Accurate variant calling is fundamental to modern genomics research and clinical sequencing. With the rise of ever-larger datasets, **speed** and **precision** are no longer optional — they are mandatory.  
**Dragen-GATK** offers an accelerated, highly-optimized pipeline for **germline variant calling**, combining Illumina's hardware acceleration and GATK’s trusted software toolkit. Let's dive into how you can set up and run **Dragen-GATK** workflows efficiently!

---

## What is Dragen-GATK?

[Dragen-GATK](https://gatk.broadinstitute.org/hc/en-us/articles/4410953761563-Introducing-DRAGMAP-the-new-genome-mapper-in-DRAGEN-GATK) is a collaboration between Illumina and the Broad Institute, combining:
- **DRAGEN’s hardware-accelerated algorithms** (available on-premises or in cloud platforms),
- with **GATK 4’s best-practice methods** for variant calling.

Dragen-GATK highlights:
- **Improved germline variant quality**, especially for indels and difficult regions.
- **Out-of-the-box compatibility** with standard GATK workflows.

---

## Why Choose Dragen-GATK?

- 🎯 **Accuracy**: Optimized algorithms for challenging regions of the genome.
- 🏥 **Clinical-grade robustness**: Used in clinical diagnostics pipelines.
- ☁️ **Cloud-ready**: Available on AWS, GCP, and other cloud platforms.
- 🛠 **Best of both worlds**: Combines DRAGEN and GATK technologies under one unified toolkit.

---

## Installing Dragen-GATK

### 🐳 Docker Local Installation

You can also use a lightweight container for Dragen-GATK. Example:

1. Create a `Dockerfile.dragmap`:

    <details>
    <summary>Example Dockerfile</summary>

    ```docker
    FROM gambalab/dragmap:latest@sha256:d1d322d87744f154bc53cd400c35bddfeff4d5787c8f6347764caf27512e3fc0

    # Install OS deps, Mambaforge, and clean up
    RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            wget \
            bash \
            bzip2 \
            ca-certificates \
            coreutils \
            tar \
        && wget -q -P /tmp \
        https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
        && bash /tmp/Miniforge3-Linux-x86_64.sh -b -p /opt/mamba \
        && rm -rf /tmp/Mambaforge.sh /var/lib/apt/lists/* \
        && apt-get clean

    # Add conda to path
    ENV PATH="/opt/mamba/bin:$PATH"
    ENV LD_LIBRARY_PATH="/opt/mamba/lib"

    # Install Python and bioinformatics tools
    RUN mamba install -y \
            -c conda-forge \
            -c bioconda \
            python=3.11 \
            samtools=1.21 \
            gatk4=4.6.1.0 \
        && mamba clean -afy
    ```
    </details>

2. Build the image:

    ```bash
    docker build -f Dockerfile.dragmap -t dragmap:1.3.0 .
    ```

3. Verify install by running:

    ```bash
    docker run --rm -it dragmap:1.3.0 gatk --help
    ```

---

## Running Dragen-GATK on Sample Data

### 📥 Download Test Data

1. **Download FASTQ files**
Follow example from previous section in FastP tutorial [here](TODO:Add href) to get a trimmed FASTQ file from the *Bacillus subtilis* ALBA01 strain.

2. **Download Reference Genome**
    - To continue with prevbious example, we will use the *Bacillus subtilis* genome from the European Nucleotide Archive (ENA).

    ```bash
    # Make data directory if it doesn't exist,
    mkdir -p data
    # Choosing the ASM904v1 B. subtilis assembly for variant calling.
    wget -nc -P ./data ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/045/GCF_000009045.1_ASM904v1/GCF_000009045.1_ASM904v1_genomic.fna.gz
    # Unzip the reference genome
    gunzip ./data/GCF_000009045.1_ASM904v1_genomic.fna.gz
    ```

3. **Create FASTA Dictionary (GATK):**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
    gatk CreateSequenceDictionary \
        -R "/app/data/GCF_000009045.1_ASM904v1_genomic.fna"'
    ```

4. **Index Reference (Samtools):**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
    samtools faidx "/app/data/GCF_000009045.1_ASM904v1_genomic.fna"'
    ```

5. **Compose STR Table (GATK):**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
    gatk ComposeSTRTableFile \
        -R "/app/data/GCF_000009045.1_ASM904v1_genomic.fna" \
        -O "/app/data/GCF_000009045.1_ASM904v1_genomic.fna.strtable"'
    ```

---

### 🚀 Variant Calling Workflow

1. **Build Hash Table**

    Before alignment, DragMap requires a hash table built from the reference:

    ```bash
    # Create a directory for the hash table
    mkdir -p data/hash_table
    # Build the hash table using DragMap
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
    dragen-os \
        --build-hash-table true \
        --ht-reference "/app/data/GCF_000009045.1_ASM904v1_genomic.fna" \
        --output-directory "/app/data/hash_table/" \
        --ht-write-hash-bin 1 \
        --num-threads 16'
    ```

2. **Map Reads and Create BAM**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
    dragen-os \
        -r "/app/data/hash_table/" \
        -1 "/app/data/SRR3317165_1.trim.fastq.gz" \
        -2 "/app/data/SRR3317165_2.trim.fastq.gz" \
        --num-threads 16 \
    | samtools view \
        --threads 16 \
        -bh -o "/app/data/SRR3317165.bam"'
    ```

3. **Prepare BAM for Variant Calling** 

    Sort the BAM file and index it:
    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
        samtools sort "/app/data/SRR3317165.bam" \
            -@ 16 \
            -o "/app/data/SRR3317165.sorted.bam"'
    ```

    Deduplicate the BAM file:
    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
        gatk --java-options "-XX:+UseG1GC -Xms4g -Xmx64g" MarkDuplicatesSpark \
            -I "/app/data/SRR3317165.sorted.bam" \
            -O "/app/data/SRR3317165.dedup.bam" \
            -M "/app/data/SRR3317165.dedup.bam.txt" \
            --conf "spark.executor.cores=16"'
    ```

    Index the deduplicated BAM file:
    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
        samtools \
            index "/app/data/SRR3317165.dedup.bam" \
            -@ 16'
    ```

4. **Calibrate DragStr Model**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
        gatk --java-options "-XX:+UseG1GC -Xms4g -Xmx64g" \
        CalibrateDragstrModel \
            -R "/app/data/GCF_000009045.1_ASM904v1_genomic.fna" \
            -I "/app/data/SRR3317165.dedup.bam" \
            -str "/app/data/GCF_000009045.1_ASM904v1_genomic.fna.strtable" \
            -O "/app/data/GCF_000009045.1_ASM904v1_genomic.model"'
    ``` 

5. **Call Variants**

    ```bash
    docker run --rm -it \
    -v "$(pwd):/app" \
    dragmap:1.3.0 \
    bash -c '
        gatk --java-options "-XX:+UseG1GC -Xms4g -Xmx64g" \
        HaplotypeCaller \
            -R "/app/data/GCF_000009045.1_ASM904v1_genomic.fna" \
            -I "/app/data/SRR3317165.dedup.bam" \
            -O "/app/data/SRR3317165.variants.vcf" \
            --native-pair-hmm-threads 16 \
            --dragen-mode true \
            --dragstr-params-path "/app/data/GCF_000009045.1_ASM904v1_genomic.model'
    ```
---

### 📂 Output Files

| File | Description | Step |
|------|-------------| -----|
| `GCF_000009045.1_ASM904v1_genomic.fna` | Reference genome | Download |
| `*.dict` | Dictionary file | GATK |
| `*.fai` | FAI index file | Samtools |
| `*.strtable` | STR table | GATK |
| `./data/hash_table` | Directory with hash files | Dragen-os |
| `SRR3317165.bam` | Aligned reads | Dragen-os |
| `SRR3317165.sorted.bam` | Sorted BAM file | Samtools |
| `SRR3317165.dedup.bam` | Deduplicated BAM file | GATK |
| `SRR3317165.dedup.bam.bai` | Index for deduplicated BAM | Samtools |
| `SRR3317165.dedup.bam.txt` | MarkDuplicates report | GATK |
| `GCF_000009045.1_ASM904v1_genomic.model` | Calibrated model | GATK |
| `SRR3317165.variants.vcf` | Called variants (VCF) | GATK |

---

## Key Dragen-GATK Parameters You Should Know

| Tool | Parameter | Purpose |
|------|-----------|---------|
| CreateSequenceDictionary | `-R` | Reference genome FASTA |
| ComposeSTRTableFile | `-R` | Reference genome FASTA |
| ComposeSTRTableFile | `-O` | Output STR table |
| dragen-os | `--build-hash-table` | Run build hash table for reference |
| dragen-os.build-hash-table | `--ht-reference` | Build hash table directory |
| dragen-os.build-hash-table | `--output-directory` | | Output directory for hash table |
| dragen-os.build-hash-table | `--ht-write-hash-bin` | Write hash bin files |
| dragen-os | `num-threads` | Number of threads to use |
| dragen-os | `-r` | Hash table directory |
| dragen-os | `-1` | Input FASTQ file 1 |
| dragen-os | `-2` | Input FASTQ file 2 |
| gatk | `--java-options` | Java options for GATK |
| gatk.MarkDuplicatesSpark | `-I` | Input BAM file |
| gatk.MarkDuplicatesSpark | `-O` | Output BAM file |
| gatk.MarkDuplicatesSpark | `-M` | MarkDuplicates report |
| gatk.MarkDuplicatesSpark | `--conf` | Spark configuration |
| gatk.CalibrateDragstrModel | `-R` | Reference genome FASTA |
| gatk.CalibrateDragstrModel | `-I` | Input deduplicated BAM file |
| gatk.CalibrateDragstrModel | `-str` | STR table file |
| gatk.CalibrateDragstrModel | `-O` | Output model file |
| gatk.HaplotypeCaller | `-R` | Reference genome FASTA |
| gatk.HaplotypeCaller | `-I` | Input deduplicated BAM file |
| gatk.HaplotypeCaller | `-O` | Output VCF file |
| gatk.HaplotypeCaller | `--native-pair-hmm-threads` | Number of threads for pair HMM |
| gatk.HaplotypeCaller | `--dragen-mode` | Enable DRAGEN mode |
| gatk.HaplotypeCaller | `--dragstr-params-path` | Path to calibrated model file |

---

## Dragen-GATK in Your Genomics Workflow

A typical NGS analysis workflow with Dragen-GATK would look like:

1. **QC**: Preprocess reads with [FastP](https://github.com/OpenGene/fastp) or similar tools.
2. **Alignment**: Map reads to reference using Dragen-GATK's BwaMemAligner.
3. **Variant Calling**: Call variants using DragenGatkCaller.
4. **Post-processing**: Perform variant filtration and annotation (e.g., with SnpEff or VEP).
5. **Interpretation**: Analyze clinically or biologically relevant variants.

---

# 🎯 Conclusion

**Dragen-GATK** provides the best of both worlds: blazing speed and rock-solid accuracy.  
If you're building high-throughput sequencing pipelines — whether for research, diagnostics, or clinical genomics — integrating Dragen-GATK will significantly boost your variant discovery pipeline’s performance.

High-quality variant calling is closer (and faster) than ever!

---

# 📚 References

- [Dragen-GATK Documentation](https://gatk.broadinstitute.org/hc/en-us/articles/4410953761563-Introducing-DRAGMAP-the-new-genome-mapper-in-DRAGEN-GATK)
- [GATK GitHub](https://github.com/broadinstitute/gatk)
- [Illumina Dragen Platform](https://www.illumina.com/products/by-type/informatics-products/dragen-bio-it-platform.html)
- [European Nucleotide Archive](https://www.ebi.ac.uk/ena/browser/home)
- [Docker Documentation](https://docs.docker.com/get-docker/)
- [Conda Documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Mamba Documentation](https://mamba.readthedocs.io/en/latest/index.html)