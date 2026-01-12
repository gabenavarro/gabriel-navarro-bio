@{id = "a3656312-e236-42a9-b7f9-6d046619ff2f"
  title = "FastPLong: Quality Control for Long Read Sequencing Data"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'bioinformatics', 'genomics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/fastplong-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE FastPLong: Quality Control for Long Read Sequencing Data

# Setting Up FastPLong with Conda and Docker

FastPLong is an ultra‑fast preprocessing and quality‑control tool for long‑read sequencing data (Nanopore, PacBio, Cyclone, etc.). It generates filtered FASTQ output along with HTML and JSON QC reports.

In this guide, we'll cover:

- Installing FastPLong via **Conda**
- Downloading the **prebuilt binary**
- Compiling from **source** (optional)
- Running FastPLong in a **Docker** container
- A simple **example** workflow using a FASTQ file

---

## 1. Prerequisites

- **Conda** (Miniconda or Anaconda) for package installs
- **Docker** (optional for containerized use)
- A sample **long‑read FASTQ** file (plain or compressed)

---

## 2. Installing FastPLong via Conda

FastPLong is available on Bioconda:

```bash
# Ensure Bioconda channel is enabled
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# Create and activate env
conda create -n fastplong_env python=3.9 -y
conda activate fastplong_env

# Install FastPLong
conda install fastplong -y
```

To upgrade later:

```bash
conda update fastplong -y
```

---

## 3. Downloading the Prebuilt Binary

For Linux users, you can grab the latest standalone binary:

```bash
# Download latest (CentOS build)
wget http://opengene.org/fastplong/fastplong \
     -O fastplong
chmod +x fastplong

# Or fetch a specific version
wget http://opengene.org/fastplong/fastplong.0.2.2 \
     -O fastplong
chmod +x fastplong
```

You can now run `./fastplong --help` to see all options.

---

## 4. Compiling from Source (Optional)

If you need the bleeding‑edge version or wish to customize:

```bash
# Install dependencies
conda install -c conda-forge libdeflate isa-l libhwy -y

# Clone & build
git clone https://github.com/OpenGene/fastplong.git
cd fastplong
make -j$(nproc)
make test
sudo make install
```

This installs `fastplong` into your system PATH.

---

## 5. Running FastPLong in Docker

To avoid local installs, use a containerized setup. Create a simple Dockerfile:

```dockerfile
# Dockerfile
FROM continuumio/miniconda3:latest

# Install FastPLong
RUN conda config --add channels defaults \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge \
    && conda install fastplong -y \
    && conda clean --all -y

ENTRYPOINT ["fastplong"]
```

Build and tag:

```bash
docker build -t fastplong:latest .
```

Run on your FASTQ:

```bash
docker run --rm -v $(pwd):/data fastplong:latest \
  -i /data/reads.fastq.gz \
  -o /data/filtered.fq.gz \
  --html /data/report.html \
  --json /data/report.json
```

---

## 6. Example Usage

### Basic command

```bash
fastplong -i reads.fastq.gz -o filtered.fq.gz
```

This applies default filters and writes:

- **`filtered.fq.gz`**: reads passing all filters
- **`fastplong.html`**: interactive HTML QC report
- **`fastplong.json`**: machine‑readable JSON report

### Common options

- **Quality filters** (default on):
  - `-m 10` (mean quality ≥Q10)
  - `-q 15 -u 40` (phred ≥15; ≤40% low‑quality bases)
- **Length filters**:
  - `-l 1000` (min length 1 kb)
  - `--length_limit 50000` (max length 50 kb)
- **Adapter trimming**:
  - `-s START_SEQ -e END_SEQ`
  - `-a adapters.fasta`
- **Streaming**:
  - `--stdout` to pipe passing reads into another tool
  - `--stdin` to read from STDIN
- **Splitting**:
  - `--split 4` (into 4 output files)
  - `--split_by_lines 100000` (100 k lines per file)

Example with more filters:

```bash
fastplong \
  -i reads.fastq.gz \
  -o filtered.fq.gz \
  --failed_out failed.fq.gz \
  -m 12 -l 500 \
  --cut_front --cut_tail \
  --split 8 \
  --html qc.html --json qc.json
```

---

## 7. Tips & Best Practices

- **Preview a subset**: use `--reads_to_process 100000` for a quick QC check.
- **Avoid overwriting**: add `--dont_overwrite` to protect existing outputs.
- **Parallelization**: combine `--threads` (via environment) with `--split` for concurrent downstream steps.
- **Low‑complexity filtering**: enable `-y` for simple repeats removal.
- **Report customization**: change titles with `-R "My FastPLong Report"`.

---

## 8. Conclusion

FastPLong streamlines long‑read QC and preprocessing, offering flexible filters, streaming, and detailed reports. Whether installed via Conda, binary, source, or Docker, you can integrate it seamlessly into your analysis pipeline.

*Happy filtering!*
