@{id = "28b30727-8521-4637-acfc-4c48747e2fe2"
  title = "Mamba State Space Model Alternative for Transformers"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'machine learning', 'deep-learning', 'transformers']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/mamba-statespace-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE


# Getting Started with Mamba-SSM in Docker

**Mamba** is a family of Structured State Space Models (SSMs) that deliver Transformer-level performance on sequence tasks with subquadratic cost. Whether you want to explore the original Mamba block (v1) or the newer Mamba-2 architecture, you can containerize your environment via Docker for reproducible, GPU-accelerated workflows.

---

## Table of Contents

1. [Why Mamba?](#why-mamba)  
2. [Prerequisites](#prerequisites)  
3. [Dockerfile Example](#dockerfile-example)  
4. [Building the Docker Image](#building-the-docker-image)  
5. [Running Mamba Inside Docker](#running-mamba-inside-docker)  
6. [Python Usage Example](#python-usage-example)  
7. [Extending to Mamba-2](#extending-to-mamba-2)  
8. [Tips & Best Practices](#tips--best-practices)  
9. [Further Resources](#further-resources)  

---

## Why Mamba?

- **Selective State Spaces**: Combines local convolution with global state propagation.  
- **High Throughput**: Leverages fast CUDA kernels (similar spirit to FlashAttention).  
- **Competitive**: Matches or exceeds Transformer performance on language modeling and other dense tasks.  

---

## Prerequisites

- **Docker** v20.10+ (with NVIDIA GPU support if you want GPU acceleration)  
- **PyTorch** 1.12+ and **CUDA** 11.6+ on the host (optional if you rely fully on the container)  
- **16 GB+ RAM** for building and running larger models  
- Basic familiarity with Docker and Python  

---

## Dockerfile Example

Create a file named `Dockerfile`:

```dockerfile
# Use an official PyTorch image with CUDA
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Avoid Python buffering and interactive prompts
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Mamba and optional causal-conv1d
RUN pip install --upgrade pip \
    && pip install mamba-ssm[causal-conv1d] \
    && rm -rf ~/.cache/pip

# Copy your application code (if any)
WORKDIR /workspace
COPY . /workspace

# Default entrypoint: launch Python REPL
ENTRYPOINT ["python"]