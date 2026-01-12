@{id = "99db6486-f2df-4608-a78e-dfd30a337c51"
  title = "Funannotate: A Tool for Genome Annotation"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'bioinformatics', 'genomics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/funannotate-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE Funannotate: A Tool for Genome Annotation

# Setting Up Funannotate with Conda and Docker

**Funannotate** is an automated genome annotation pipeline primarily designed for fungi, but it can also handle higher eukaryotes. It orchestrates repeat masking, gene prediction, and functional annotation into a streamlined workflow.

This guide covers:

1. Prerequisites
2. Installing Funannotate via Conda (Bioconda)
3. Quickstart with Docker
4. Optional: Installing GeneMark-ES/ET
5. Example Workflows
   - Genome + RNA-seq annotation
   - Genome-only annotation
6. Tips & Best Practices
7. Further Resources

---

## 1. Prerequisites

- **Conda** (Miniconda or Anaconda) for package management
- **Docker** (optional) for containerized runs
- **Genome assembly** (FASTA) of your target organism
- **RNA-seq FASTQ** files (paired or single-end) for evidence-based annotation (optional)
- Familiarity with basic command-line operations

---

## 2. Installing Funannotate via Conda

The recommended install uses Bioconda channels. If dependency resolution is slow, consider replacing `conda` with `mamba`.

```bash
# Configure channels
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# Create and activate environment
conda create -n funannotate_env "python>=3.6,<3.9" funannotate -y
conda activate funannotate_env
```

> **Tip:** If solving is slow:
> ```bash
> conda install -n base mamba -y
> mamba create -n funannotate_env funannotate -y
> ```

To update:
```bash
conda update funannotate -y
```

---

## 3. Quickstart with Docker

A Docker image with Funannotate and required databases is available.

```bash
# Pull the full image (with databases)
docker pull nextgenusfs/funannotate

# (Optional) Download the provided bash wrapper
wget -O funannotate-docker \
  https://raw.githubusercontent.com/nextgenusfs/funannotate/master/funannotate-docker
chmod +x funannotate-docker

# Run a command, e.g. predict step with 12 CPUs
./funannotate-docker predict -t predict --cpus 12
```

If you prefer a slim image (no databases):
```bash
docker pull nextgenusfs/funannotate-slim
```
You can use `docker run` directly or via the `funannotate-docker` wrapper to automatically bind volumes and retain your user permissions.

---

## 4. Optional: Installing GeneMark-ES/ET

GeneMark is not distributable via Bioconda. To enable GeneMark support:

1. Register and download from [GeneMark license page](http://topaz.gatech.edu/GeneMark/license_download.cgi).
2. Extract and edit shebangs of Perl scripts to use `/usr/bin/env perl`.
3. Add the `gmes_petap.pl` directory to your `$PATH`, or set:
   ```bash
   export GENEMARK_PATH=/path/to/gmes_petap
   ```

Without GeneMark, Funannotate will rely on BUSCO/Augustus for ab initio predictions.

---

## 5. Example Workflows

### 5.1 Genome + RNA-seq Annotation

Assume files in working directory:
```
assembly.fasta
left_R1.fq.gz   right_R1.fq.gz
left_R2.fq.gz   right_R2.fq.gz
nanopore_rna.fq.gz
```

```bash
# 1) Clean and sort assembly
funannotate clean -i assembly.fasta --minlen 1000 -o assembly.clean.fa
funannotate sort -i assembly.clean.fa -b scaffold -o assembly.sorted.fa

# 2) Mask repeats
funannotate mask -i assembly.sorted.fa --cpus 12 -o assembly.masked.fa

# 3) Train with RNA-seq
funannotate train \
  -i assembly.masked.fa \
  --left left_R1.fq.gz,right_R1.fq.gz \
  --right left_R2.fq.gz,right_R2.fq.gz \
  --nanopore_mrna nanopore_rna.fq.gz \
  --stranded RF --jaccard_clip \
  --species "MySpecies" --strain "StrainA" \
  --cpus 12 -o fun_run

# 4) Predict gene models
funannotate predict -i assembly.masked.fa \
  --species "MySpecies" --strain "StrainA" \
  --cpus 12 -o fun_run

# 5) Update UTRs and refine gene models
funannotate update -i fun_run --cpus 12

# 6) Functional annotation
funannotate iprscan -i fun_run -m docker --cpus 12
funannotate annotate -i fun_run --cpus 12
```

Results appear under `fun_run/predict_results`, `fun_run/update_results`, and `fun_run/annotate_results`.

### 5.2 Genome-Only Annotation

Without RNA data, skip train/update and use BUSCO seed species:

```bash
# Mask repeats
funannotate mask -i assembly.fasta --cpus 12 -o assembly.masked.fa

# Predict with BUSCO-based training
funannotate predict \
  -i assembly.masked.fa \
  --species "MySpecies" --strain "StrainA" \
  --busco_seed_species botrytis_cinerea \
  --cpus 12 -o fun_run_genome_only

# Functional annotation
funannotate annotate -i fun_run_genome_only --cpus 12
```

---

## 6. Tips & Best Practices

- **`--dont_overwrite`**: protect existing outputs.
- **Resume pipeline**: use `--resume` if interrupted.
- **Metagenomes**: add `--meta` in `predict` step for uneven coverage.
- **Max intron length**: adjust with `--max_intronlen` for non-fungal genomes.
- **Repeat-aware EVM**: use `--repeats2evm` in predict to reduce false positives in large genomes.

---

## 7. Further Resources

- **Funannotate docs:** http://funannotate.readthedocs.io
- **GitHub:** https://github.com/nextgenusfs/funannotate
- **Bandage** for GFA visualization: https://github.com/rrwick/Bandage

---

*Happy annotating!*
