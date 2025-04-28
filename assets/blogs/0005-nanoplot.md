@{id = "11035607-63d6-46cf-a8ea-daf2384569a7"
  title = "NanoPlot: Quality Control for Nanopore Sequencing Data"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'bioinformatics', 'genomics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/nanoplot-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = true
}
# TODO: COMPLETE Mastering Quality Control in Omics with NanoPlot

# Setting Up NanoPlot with Conda and Docker

NanoPlot is a powerful plotting tool for long‑read sequencing data and alignments. It generates publication‑quality visualizations (e.g., read length histograms, quality plots, bivariate scatter plots) and a comprehensive HTML summary.

In this guide, we'll cover:

- Installing NanoPlot via **Conda**
- Running NanoPlot in a **Docker** container
- A simple **example** workflow using a FASTQ file

---

## 1. Prerequisites

- **Python 3.6+** (for Conda installation)
- **Conda** (Miniconda or Anaconda)
- **Docker** (if using the containerized approach)
- A sample **FASTQ** file from your long‑read sequencing run

---

## 2. Installing NanoPlot with Conda

The NanoPlot package is available on Bioconda. First, ensure you have the `bioconda` channel enabled:

```bash
# Add channels if not already present
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# Create (or activate) your analysis environment
conda create -n nanoplot_env python=3.9 -y
conda activate nanoplot_env

# Install NanoPlot
conda install nanoplot -y
```

To upgrade later:

```bash
conda update nanoplot -y
```

---

## 3. Running NanoPlot in Docker

If you prefer containerized workflows (no local Python setup), you can run NanoPlot via Docker:

1. **Pull** the official NanoPlot image (if available) or build your own.

   ```bash
   # Pull from Docker Hub (hypothetical image)
   docker pull quay.io/biocontainers/nanoplot:latest
   ```

2. **Build** a simple Dockerfile (if no pre-built image is available):

   ```dockerfile
   # Dockerfile
   FROM continuumio/miniconda3:latest

   # Install NanoPlot from Bioconda
   RUN conda config --add channels defaults \
       && conda config --add channels bioconda \
       && conda config --add channels conda-forge \
       && conda install nanoplot -y \
       && conda clean --all -y

   # Set entrypoint
   ENTRYPOINT ["NanoPlot"]
   ```

   Build it:

   ```bash
   docker build -t nanoplot:latest .
   ```

3. **Run** NanoPlot on your data:

   ```bash
   docker run --rm -v $(pwd):/data nanoplot:latest \
     --fastq /data/reads.fastq.gz \
     --outdir /data/nanoplot_output \
     --prefix myrun_
   ```

This mounts your current directory into the container (`/data`) and outputs results back to your host system.

---

## 4. Example Usage

Assume you have a compressed FASTQ file `reads.fastq.gz` in your working directory.

### 4.1 Quick Run (Conda)

```bash
# Activate environment
conda activate nanoplot_env

# Plot read length histogram and bivariate quality plot
NanoPlot \
  --fastq reads.fastq.gz \
  --loglength \
  -o nanoplot_results \
  --prefix sample1_
```

### 4.2 Docker Run

```bash
docker run --rm -v $(pwd):/data nanoplot:latest \
  --fastq /data/reads.fastq.gz \
  --loglength \
  --outdir /data/nanoplot_results \
  --prefix sample1_
```

After completion, you’ll find:

- `sample1_STATS.html` — interactive HTML report
- Multiple PNG/SVG plots:
  - Read length histogram
  - Log-transformed length histogram
  - Length vs. quality scatter (hex/kde)
  - Quality over time
  - And more…

---

## 5. Tips & Tricks

- **Threads**: use `-t N` or `--threads N` to speed up processing on multicore machines.
- **Filtering**: drop short or low-quality reads with `--minlength 1000` or `--minqual 7`.
- **Custom plots**: specify formats (`-f pdf svg`) and plot types (`--plots dot hex`).
- **Store data**: use `--store` to save extracted metrics in a pickle for downstream analyses.

---

## 6. Conclusion

NanoPlot makes visualizing long‑read sequencing data straightforward, whether via Conda or Docker. With a few simple commands you can generate publication‑ready figures and detailed HTML reports.

Feel free to explore more options in the [NanoPlot documentation](https://github.com/wdecoster/NanoPlot) and customize your workflow!

---

*Happy plotting!*
