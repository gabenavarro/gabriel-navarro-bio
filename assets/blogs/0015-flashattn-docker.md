@{id = "54eb9b1c-0da3-4903-b126-ef6411072c5c"
  title = "Reproducibility in ML with Docker"
  date = "2025-05-10T00:00:00Z"
  tags = ['docker', 'machine learning']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/reproducibility-in-ml-with-docker-thumb.svg"
  description = "Learn how to use Docker to ensure reproducibility in machine learning projects, from local development to production deployment."
  type = "note"
  disabled = False
}


# Reproducibility in ML with Docker

Machine learning has delivered remarkable breakthroughs, from beating humans at Go to powering life-saving medical diagnoses. Yet amid this progress lurks a nagging problem: **reproducibility**. You train a model on your machine and achieve 92% accuracy. You share your code and data—only to hear crickets when colleagues try to reproduce your results. Why? Subtle differences in library versions, CUDA drivers, or even Python patch levels can send your metrics spiraling. As ML workloads grow in complexity—mixing Python packages, C++ extensions, GPU drivers, and cloud services. The “it works on my laptop” excuse no longer cuts it.

Containerization, and Docker in particular, offers a compelling antidote. By packaging code, dependencies, and runtime into a self-contained image, you lock down your environment once and for all. But how do you wield Docker effectively for ML? Let’s dive in.

---

## 1. Docker Basics for ML Practitioners

At its core, Docker lets you build **images**, immutable snapshots containing everything your code needs, and run them as **containers**, lightweight virtualized processes that behave identically across hosts.

* **Image**: A layered filesystem plus metadata.
* **Container**: A running instance of an image.
* **Dockerfile**: A recipe that describes how to assemble an image step by step.

Typical workflow:

1. **Write a Dockerfile**: start from a base image (`python:3.10`, `nvcr.io/nvidia/pytorch`, etc.).
2. **Build**: `docker build -t my-ml-image .`
3. **Run**: `docker run --gpus all -it my-ml-image bash`

This ensures your code always sees the same OS libraries, Python packages, and—even GPU drivers—regardless of where you run it.

---

## 2. Creating an Ideal ML Development Environment with Docker

A well-crafted ML dev container should feel as seamless as a local virtualenv, yet fully reproducible. Key considerations:

* **Interactive shells**: preload your virtualenv, IPython, and tools like `ruff` or `black`.
* **Port forwarding**: expose Jupyter or TensorBoard ports.
* **Volume mounts**: mount your source code (`-v $(pwd):/workspace`) so you can iterate without rebuilding every change.
* **User permissions**: avoid running as `root` inside the container to prevent file-permission headaches.

**Example `docker-compose.yml`** for local dev:

```yaml
version: '3.8'
services:
  ml-dev:
    image: my-flash-attn:latest # Dockerfile example below
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - .:/workspace
    ports:
      - "8888:8888"   # Jupyter
      - "6006:6006"   # TensorBoard
    working_dir: /workspace
    user: "${UID}:${GID}"
```

This lets you `docker-compose up` and jump straight into coding with GPU support, linting, notebooks, and your editor talking to a containerized runtime.

---

## 3. Designing Dockerfiles for ML Training Workloads

Production and heavy-duty training images need more careful layering for cache efficiency and minimal size. Here’s a pattern I often use:

1. **Base image selection**

   * For GPU training: NVIDIA’s PyTorch container (`nvcr.io/nvidia/pytorch:xx.xx-py3`) or `nvidia/cuda:xx.x-cudnn8-runtime-ubuntu20.04`.

2. **System dependencies**

   ```dockerfile
   RUN apt-get update && \
       apt-get install -y --no-install-recommends \
         build-essential git curl && \
       rm -rf /var/lib/apt/lists/*
   ```
3. **Python dependencies**

   * Separate “core” vs. “dev” installs so rebuilds only reinstall what changed.

4. **Source code**

   * Copy only what you need, use `.dockerignore` aggressively.

**Layering tip**: group seldom-changing steps (OS packages, complex library builds) before frequently updated steps (your code), so Docker’s cache accelerates iterative workflows.

---

## 4. Managing Dependencies and GPU Access

### Pinning and Version Control

* Always pin Python packages (e.g., `torch==2.1.0`) in your Dockerfile or a `requirements.txt`.
* Consider hashing your dependencies: `pip install --require-hashes -r requirements.txt`.

### GPU Access

Docker integrates with NVIDIA GPUs through the **NVIDIA Container Toolkit**. Essentials:

1. **Install** the nvidia-docker runtime on the host.
2. **Base image** must include CUDA libraries that match the host driver.
3. **Run command**:

   ```bash
   docker run --gpus '"device=0,1"' -e NCCL_SOCKET_IFNAME=^docker0,lo \
     my-ml-image nvidia-smi
   ```
4. **Environment variables**:

   * `NCCL_SOCKET_IFNAME` to optimize multi-GPU communication over the correct network interface.
   * `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128` for out-of-memory tuning.

---

## 5. Case Study: From Local Development to Production Deployment of flash-attn Repository

Let’s walk through a real example: containerizing the **flash-attn** repository for both local experimentation and large-scale cloud training.

<details>
<summary><strong>Dockerfile for flash-attn (click to expand)</strong></summary>

```dockerfile
FROM nvcr.io/nvidia/pytorch:25.01-py3

WORKDIR /workdir

# 1. Build flash-attn from source
RUN rm -rf ./flash-attention/* && \
    pip uninstall flash_attn -y && \
    git clone -b v2.7.4.post1 https://github.com/Dao-AILab/flash-attention.git && \
    cd flash-attention/csrc/rotary && python setup.py install && \
    cd ../layer_norm && python setup.py install && \
    cd ../fused_dense_lib && python setup.py install && \
    cd ../fused_softmax && python setup.py install && \
    cd ../../ && python setup.py install

# 2. Install ML & dev dependencies
RUN pip install --no-cache-dir \
    lightning tensorboard pydantic \
    ipykernel ruff nbformat ipywidgets tqdm \
    synapseclient datasets litdata \
    google-cloud-aiplatform google-cloud-pipeline-components db-dtypes

# 3. Optimize NCCL for Docker networking
ENV NCCL_SOCKET_IFNAME=^docker0,lo

# 4. Switch to app directory & add healthcheck
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD nvidia-smi || exit 1
```

</details>

### Analysis

* **Base image**: NVIDIA’s optimized PyTorch runtime brings CUDA, cuDNN, and NCCL out of the box.
* **Layer ordering**: Flash-attn’s C++ builds sit in their own `RUN` block—only change when upgrading the library.
* **Dev vs. Prod**: You can split dev tools (linters, notebooks) into a separate stage or image to keep production slim.
* **Healthcheck**: Automatically verifies GPU availability inside your container.

### From Local to Cloud

1. **Local builds**:

   ```bash
   docker build -t flash-attn:local -f Dockerfile .
   ```

   Once built, you can run the container locally:

   ```bash
   docker run --gpus all -it flash-attn:local bash
   ```
   * Test GPU access with `nvidia-smi`.
   * Run a sample script (e.g., `python flash_example.py`) to validate FlashAttention functionality.

2. **Push to registry**:

   ```bash
   docker tag flash-attn:local myrepo/flash-attn:1.0.0
   docker push myrepo/flash-attn:1.0.0
   ```

3. **Deploy to cloud**:
	* Use a cloud service (e.g., GCP, AWS) to pull the image and run it on a multi-GPU instance.
	* Leverage orchestration tools (Kubernetes, Docker Swarm) for scaling and managing multiple containers.

   Specifically, for GCP, you can use the AI Platform to create a custom training job with your Docker image. This allows you to run distributed training across multiple GPUs seamlessly.

   In later posts, we’ll explore how to set up a GCP training job using the flash-attn image. For now, the focus is on the Docker pipeline. As a teaser, here’s a snippet of how you might configure a GCP training job:

	<details>
	<summary><strong>Dockerfile for flash-attn (click to expand)</strong></summary>

	```python
	from google.cloud import aiplatform
	from google.oauth2 import service_account
	import os

	# Vertex AI Configuration
	SERVICE_KEY_PATH = os.getenv(
		"GOOGLE_APPLICATION_CREDENTIALS", 
		"/path/to/your/service_account_key.json"
	)
	LOCATION = "your-gcp-region"         # e.g., "us-central1"
	ZONE = "your-gcp-zone"               # e.g., "us-central1-a"
	PROJECT_ID = "your-gcp-project-id"   # e.g., "my-project-12345"
	RESERVATION_TYPE = "ANY"             # or "ANY_RESERVATION"
	STAGING_BUCKET = "gs://your-gcp-training-bucket/flash-attn-example/staging"
	SERVICE_ACCOUNT = f"vertex-ai@{PROJECT_ID}.iam.gserviceaccount.com"
	TRAIN_IMAGE = f"your-location-docker.pkg.dev/{PROJECT_ID}/repositories/flash-attention:latest"
	DISPLAY_NAME = "flash-attn-crypto-model-training"

	# Hardware Configuration
	NODES = 1
	MACHINE_TYPE = "a3-megagpu-8g"
	ACCELERATOR_TYPE = "NVIDIA_H100_MEGA_80GB"
	ACCELERATOR_COUNT = 8

	# Training Command
	CMD = [
		"python3", 
		"/gcs/your-gcp-training-bucket/flash-attn-example/scripts/flash_attn_train.py",
		"--config", 
		"/gcs/your-gcp-training-bucket/flash-attn-example/config/flash_attn_crypto_model_config.yaml",
	]

	# Worker pool specification
	worker_pool_specs=[
		{
			"replica_count": NODES,
			"machine_spec": {
				"machine_type": MACHINE_TYPE,
				"accelerator_type": ACCELERATOR_TYPE,
				"accelerator_count": ACCELERATOR_COUNT,
				"reservation_affinity": {
					"reservation_affinity_type": RESERVATION_TYPE,
				}
			},
			"container_spec": {
				"image_uri": TRAIN_IMAGE,
				"command": CMD
			}
		}
	]

	# Initialize Vertex AI
	aiplatform.init(
		project=PROJECT_ID,
		location=LOCATION,
		credentials=service_account.Credentials.from_service_account_file(
			SERVICE_KEY_PATH
		)
	)

	# Create and submit the training job
	job = aiplatform.CustomJob(
		display_name=DISPLAY_NAME, 
		worker_pool_specs=worker_pool_specs,
		staging_bucket=STAGING_BUCKET,
	)

	job.submit(
		service_account=SERVICE_ACCOUNT
	)

	# Print job details
	print(f"Job ID: {job.resource_name}")
	print(f"Job state: {job.state}")
	```

	</details>

   * This code snippet initializes a Vertex AI custom job with the flash-attn image, specifying the machine type, accelerator type, and training command. It also sets up the necessary service account and staging bucket for GCP.

This pipeline—from a reproducible local Docker build to a scalable multi-GPU cluster—ensures consistency and dramatically lowers the “it runs here” friction.

---

## 6. Best Practices and Common Pitfalls

**Best Practices**  
- **Pin all dependencies**, including OS packages.  
- Use **multi-stage builds** to separate build-time from run-time artifacts.  
- Leverage **cached layers**: group heavy installs before your frequent code changes.  
- Maintain a **.dockerignore** to exclude logs, data, and other bloat.  
- **Scan images** for vulnerabilities (e.g., `docker scan`).  
- Automate builds & scans in CI (GitHub Actions, GitLab CI).

**Common Pitfalls**  
- **Huge images**: piling on dev tools or data can push images to hundreds of gigabytes—slow to pull and costly to store. As a baseline measurement, most base images with CUDA and PyTorch are around 8 GB. Then add your dependencies.
- **Driver mismatch**: CUDA version in image vs. host driver mismatch leads to “libcudart.so” errors. For the most part, as long as you use a CUDA version that is older than the driver version, you should be fine, but you are likely to run into issues if you use a newer CUDA version than the driver version. When running locally, use `nvidia-smi` to check the driver version. For cloud, ensure your service provider supports the required CUDA version. 
- **No health checks**: silent GPU failures can derail long-running jobs without alerting you.  
- **Overlooking secrets**: never bake API keys or credentials into images; use environment variables or secret managers.

---

## Conclusion and Resources for Further Learning

Docker transforms ML workflows by locking down environments from local dev through production. It tackles the reproducibility crisis head-on and scales effortlessly, whether on your workstation or a GPU cluster. By following best practices—pinning dependencies, optimizing layers, and managing GPU access—you’ll save countless hours chasing elusive bugs.

**Further Reading**  
- Docker Documentation: https://docs.docker.com  
- NVIDIA Container Toolkit: https://github.com/NVIDIA/nvidia-docker  
- Best Practices for Writing Dockerfiles: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/  
- flash-attn GitHub: https://github.com/Dao-AILab/flash-attention  

With a solid containerization strategy, your ML projects will be as reproducible as they are performant. Happy containerizing!