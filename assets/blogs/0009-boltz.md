@{id = "210d3bac-6c2f-414f-bbee-6480db899ae0"
  title = "Boltz‑1x: A Guide to Protein Folding"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'protein folding', 'bioinformatics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/botlz1x-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE 

# Setting Up Boltz‑1x with Docker

**Boltz‑1x** is an open‑source, MIT‑licensed model suite for predicting biomolecular structures—proteins, RNA, DNA, covalent ligands, glycans, and more. It supports modified residues and allows conditioning on interaction pockets or contacts.

This guide covers:

1. Prerequisites
2. (Optional) Local installation via pip
3. Building a Docker image
4. Running inference with Docker
5. Example usage
6. Tips & Best Practices
7. Further Resources

---

## 1. Prerequisites

- **Docker** (v20.10+) installed and running
- A directory of **input files** (FASTA, YAML, or a folder containing both)
- (Optional) **MSA server** or internet access for on‑the‑fly MSA generation
- Familiarity with basic command‑line operations

---

## 2. (Optional) Local Installation via pip

If you prefer running locally in a Python environment:

```bash
# Create a fresh virtual environment
python -m venv boltz_env
source boltz_env/bin/activate

# Install the latest release
pip install boltz -U

# Or install bleeding‑edge directly from GitHub
git clone https://github.com/jwohlwend/boltz.git
cd boltz
pip install -e .
```

Once installed, you can invoke:

```bash
boltz predict path/to/input.fasta --use_msa_server
```

---

## 3. Building a Docker Image

To containerize Boltz‑1x, create a `Dockerfile` like below:

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install Boltz and its dependencies
RUN pip install --no-cache-dir boltz -U

# Set working directory
WORKDIR /app

# Default entrypoint
ENTRYPOINT ["boltz"]
```

Build the image:

```bash
docker build -t boltz:1x .
```

---

## 4. Running Inference with Docker

Assume your local directory has:
```
/myproject
├── input/         # folder containing FASTA or YAML files
└── output/        # directory for prediction outputs
```

Run Boltz‑1x via Docker:

```bash
docker run --rm \
  -v $(pwd)/input:/data/input \
  -v $(pwd)/output:/data/output \
  boltz:1x predict /data/input \
    --use_msa_server \
    --output_dir /data/output
```

- `--use_msa_server`: queries an external MSA service (internet required)
- `--output_dir`: directory where JSON/PDB results will be saved

---

## 5. Example Usage

For a single FASTA file `protein.fasta`:

```bash
docker run --rm \
  -v $(pwd)/protein.fasta:/data/protein.fasta \
  -v $(pwd)/out:/data/out \
  boltz:1x predict /data/protein.fasta \
    --use_msa_server \
    --output_dir /data/out
```

Outputs in `/data/out`:

- `protein_pred_*.pdb`: predicted 3D structures
- `protein_pred_*.json`: confidence metrics and metadata

To batch‑process a folder of FASTA/YAML:

```bash
docker run --rm \
  -v $(pwd)/inputs:/data/inputs \
  -v $(pwd)/batch_out:/data/batch_out \
  boltz:1x predict /data/inputs \
    --use_msa_server \
    --output_dir /data/batch_out
```

---

## 6. Tips & Best Practices

- **Fresh builds**: rebuild your Docker image after upgrading `boltz` via pip to pick up the latest weights.  
- **YAML inputs**: use the YAML schema for complex multi‑chain or ligand‑conditioned runs.  
- **Resource limits**: you can pass `--max_recycle N` or `--diffusion_steps M` to control CPU/GPU usage.  
- **MSA caching**: if using an external MSA server, cache `.a3m` files locally to avoid repeated downloads.  
- **Reproducibility**: pin your Docker image to a specific tag (e.g. `boltz:1x_v0.3.2`) for consistent results.

---

## 7. Further Resources

- **GitHub**: https://github.com/jwohlwend/boltz  
- **Technical report**: see the model paper linked in the repo’s README  
- **Slack**: join the Boltz‑1 community Slack channel for support and updates

---

*Happy predicting with Boltz‑1x!*

