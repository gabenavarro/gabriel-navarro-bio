@{id = "7b774e87-fbcb-423c-969b-268d8b4d47d5"
  title = "RFDiffusion: Protein Design with Diffusion Models"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'protein folding', 'bioinformatics']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/rfdifussion-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE

# Setting Up RFdiffusion with Docker

**RFdiffusion** is an open‑source diffusion model for protein structure generation and design. It supports:

- Unconditional monomer generation
- Motif scaffolding
- Symmetric oligomer design (Cyclic, Dihedral, Tetrahedral)
- Binder (PPI) design with hotspot control
- Partial diffusion & design diversification

This guide walks through:
1. Prerequisites
2. Cloning and downloading model weights
3. Writing a Dockerfile
4. Building the Docker image
5. Running RFdiffusion via Docker
6. Example: Motif scaffolding
7. Tips & Best Practices

---

## 1. Prerequisites

- **Docker** (v20.10+) with GPU support (optional but recommended)
- **nvidia-docker2** if using NVIDIA GPUs
- **~10–20 GB** disk space for model weights
- Familiarity with the command line and basic protein files (FASTA/PDB)

---

## 2. Clone & Download Model Weights

```bash
# Clone the RFdiffusion repo
git clone https://github.com/RosettaCommons/RFdiffusion.git
cd RFdiffusion

# Create a folder for weights
mkdir -p models
cd models

# Download core checkpoints
wget http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/60f09a193fb5e5ccdc4980417708dbab/Complex_Fold_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/74f51cfb8b440f50d70878e05361d8f0/InpaintSeq_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/76d00716416567174cdb7ca96e208296/InpaintSeq_Fold_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/5532d2e1f3a4738decd58b19d633b3c3/ActiveSite_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/12fc204edeae5b57713c5ad7dcb97d39/Base_epoch8_ckpt.pt

# Optional beta binder model
wget http://files.ipd.uw.edu/pub/RFdiffusion/f572d396fae9206628714fb2ce00f72e/Complex_beta_ckpt.pt

cd ../
```

---

## 3. Dockerfile

Create `docker/Dockerfile` with the following contents:

```dockerfile
# Base image with Python and CUDA
FROM nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04

# Install essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    git python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Copy RFdiffusion code and weights
WORKDIR /app
COPY . /app

# Install RFdiffusion and dependencies
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -e . && \
    pip install hydra-core==1.1.1

# Default entrypoint
ENTRYPOINT ["/app/venv/bin/python3", "scripts/run_inference.py"]
```

---

## 4. Build the Docker Image

From the repository root:

```bash
docker build -f docker/Dockerfile -t rfdiffusion:latest .
```

Use `--build-arg` if you need to pass custom CUDA or Python versions.

---

## 5. Running RFdiffusion via Docker

Mount your weights, inputs, and outputs into the container.

```bash
# Prepare directories
dkdir -p $HOME/rfd_models $HOME/rfd_inputs $HOME/rfd_outputs

# Copy downloaded weights into $HOME/rfd_models
# Place any PDB/FASTA inputs in $HOME/rfd_inputs

# Run an unconditional monomer design of length 150 (10 designs)

docker run --rm --gpus all \
  -v $HOME/rfd_models:/app/models \
  -v $HOME/rfd_inputs:/app/inputs \
  -v $HOME/rfd_outputs:/app/outputs \
  rfdiffusion:latest \
  'contigmap.contigs=[150-150]' \
  inference.output_prefix=/app/outputs/monomers \
  inference.num_designs=10
```

- **`contigmap.contigs=[L-L]`**: length range for chain
- **`inference.output_prefix`**: output directory + filename prefix
- **`inference.num_designs`**: how many designs to sample

---

## 6. Example: Motif Scaffolding

Assume you have a motif in `inputs/motif.pdb`, residues A30–A45.

```bash
docker run --rm --gpus all \
  -v $HOME/rfd_models:/app/models \
  -v $HOME/rfd_inputs:/app/inputs \
  -v $HOME/rfd_outputs:/app/outputs \
  rfdiffusion:latest \
  inference.input_pdb=/app/inputs/motif.pdb \
  'contigmap.contigs=[20-30/A30-45/20-30]' \
  inference.output_prefix=/app/outputs/scaffolded \
  inference.num_designs=5
```

This builds 20–30 AA on both sides of your motif, sampling varied loop lengths.

---

## 7. Tips & Best Practices

- **Cache IGSO3**: the first run computes geometric caches—subsequent runs are faster.
- **Symmetric designs**: use `--config-name symmetry` and `inference.symmetry=c4|d2|tetrahedral`.
- **Hotspots for binders**: set `ppi.hotspot_res=[A45,A47,A50]` for targeted PPI.
- **Partial diffusion**: add `diffuser.partial_T=<steps>` to explore around a seed structure.
- **Checkpoint overrides**: e.g. use `inference.ckpt_override_path=models/ActiveSite_ckpt.pt` for small motifs.
- **Output artifacts**: look in `/traj/` for per‑step PDBs and `.trb` for metadata.

---

*Happy protein designing with RFdiffusion!*
