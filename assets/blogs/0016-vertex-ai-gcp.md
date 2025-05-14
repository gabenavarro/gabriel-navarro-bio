@{id = "eacbeecc-3062-4bd4-83a7-8671829caaea"
  title = "Scaling Your ML Training with Vertex AI Custom Jobs on GCP"
  date = "2025-05-14T00:00:00Z"
  tags = ['cloud', 'gcp', 'machine learning']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/vertex-ai-thumb.svg"
  description = "This blog is a step-by-step guide to scaling machine learning training with Vertex AI Custom Jobs on Google Cloud, covering Docker image creation, data upload, job submission, and GPU optimization for efficient cloud-based workflows."
  type = "note"
  disabled = "true"
}
# Scaling Your ML Training with Vertex AI Custom Jobs on GCP

<p align="center">
  <img src="https://storage.googleapis.com/gn-portfolio/images/vertex-ai-thumb.svg" max-width="700">
</p>

*By Gabriel Navarro* <br/>
May 14, 2025 <br/>

---

## Introduction

As your models grow in size and complexity, you’ll inevitably hit the limits of local GPUs. Google Cloud’s Vertex AI lets you offload heavy training workloads to managed clusters of GPUs—so you can scale seamlessly, track experiments in the cloud, and integrate with the rest of GCP. In this tutorial, we’ll turn our FlashAttention‐powered Transformer example into a Vertex AI Custom Job, walking through:

1. **Building & pushing** a Docker image  
2. **Uploading** configs, code, and data to Cloud Storage  
3. **Submitting** a Custom Job via the Python SDK  
4. **Optionally** targeting reserved GPU capacity  

Let’s get started!

---

## Prerequisites

Before you begin, make sure you have:

- A **GCP project** with the **Vertex AI API** enabled  
- A **service account** vested with Vertex AI & Storage permissions  
- The service account’s JSON key, and `GOOGLE_APPLICATION_CREDENTIALS` pointing to it  
- **Docker** and the **gcloud** CLI installed  

> 🔑 If you haven’t set up your GCP project or service account yet, follow [GCP Setup](https://cloud.google.com/vertex-ai/docs/general/setup) first.

---

## 1. Build & Push Your Docker Image

We’ll reuse the same FlashAttention Dockerfile from local dev—just target Artifact Registry:

```bash
# Authenticate Docker to Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Clone the repo with the Dockerfile (or use your own repo)
git clone https://github.com/gabenavarro/MLContainerLab.git && \
  cd MLContainerLab

# Build your image
docker build -f ./assets/build/Dockerfile.flashattn.cu128py26cp312 \
  -t us-central1-docker.pkg.dev/my-project/repo/flash-attention:latest .

# Push it up
docker push us-central1-docker.pkg.dev/my-project/repo/flash-attention:latest

# Verify
gcloud artifacts docker images list us-central1-docker.pkg.dev/my-project/repo/flash-attention
```

> **Tip:** Replace `us-central1` and `my-project/repo` with your GCP region & Artifact Registry names.

---

## 2. Upload Config, Scripts & Data to Cloud Storage

Vertex AI jobs pull code and data from GCS. Let’s create buckets and upload everything:

```bash
# Make a bucket (if you haven’t already)
gsutil mb -l us-central1 gs://flashattn-example

# Create folder structure
gsutil mkdir \
  gs://flashattn-example/config \
  gs://flashattn-example/scripts \
  gs://flashattn-example/datasets \
  gs://flashattn-example/checkpoints \
  gs://flashattn-example/staging

# Upload model config
gsutil cp ./assets/test-files/flash-attn-config.yaml \
  gs://flashattn-example/config/

# Upload training script
gsutil cp ./scripts/flash_attn_train.py \
  gs://flashattn-example/scripts/

# Upload processed dataset, 
# Please follow the instructions in MLContainerLab to generate the dataset
# https://github.com/gabenavarro/MLContainerLab/blob/main/documentation/flash-attn.ipynb
# (or use your own)
gsutil -m cp -r ./datasets/auto_regressive_processed_timeseries \
  gs://flashattn-example/datasets/

# Inspect your uploads
gsutil ls -R gs://flashattn-example
```

---

## 3. Submit a Vertex AI Custom Job

Now we glue it all together with the Python client. This snippet:

* **Points** to our container image
* **Defines** 8× H100 GPUs (A3 MegaGPU)
* **Runs** our training script with the YAML config

```python
from google.cloud import aiplatform
from google.oauth2 import service_account
import os

# ——— Configuration ———
PROJECT_ID  = "my-project"
REGION      = "us-central1"
BUCKET      = "gs://flashattn-example"
IMAGE_URI   = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/repo/flash-attention:latest"
SERVICE_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SERVICE_ACCT= f"vertex-ai@{PROJECT_ID}.iam.gserviceaccount.com"
DISPLAY     = "flash-attn-crypto-training"

# Command to launch inside container
CMD = [
    "python3",
    "/gcs/flashattn-example/scripts/flash_attn_train.py",
    "--config", "/gcs/flashattn-example/config/flash_attn_crypto_model_config.yaml",
]

# GPU machine spec
worker_pool_specs = [
    {
        "replica_count": 1,
        "machine_spec": {
            "machine_type": "a3-megagpu-8g",
            "accelerator_type": "NVIDIA_H100_MEGA_80GB",
            "accelerator_count": 8,
            "reservation_affinity": { "reservation_affinity_type": "ANY" }
        },
        "container_spec": {
            "image_uri": IMAGE_URI,
            "command": CMD
        }
    }
]

# Initialize Vertex AI
aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
    credentials=service_account.Credentials.from_service_account_file(SERVICE_KEY)
)

# Create & submit the CustomJob
job = aiplatform.CustomJob(
    display_name=DISPLAY,
    worker_pool_specs=worker_pool_specs,
    staging_bucket=BUCKET + "/staging"
)
job.submit(service_account=SERVICE_ACCT)

print(f"Submitted: {job.resource_name}")
```

Once you run this, Vertex AI will spin up your H100 cluster, pull the container, and kick off training—complete with logs in the GCP console.

---

## 4. (Optional) Pin to a Specific Reservation

If your organization has dedicated GPU reservations, swap `reservation_affinity` to lock onto them:

```python
"reservation_affinity": {
  "reservation_affinity_type": "SPECIFIC_RESERVATION",
  "key": "compute.googleapis.com/reservation-name",
  "values": [
    f"projects/{PROJECT_ID}/zones/us-central1-a/reservations/my-h100-resv"
  ]
}
```

This guarantees your job runs on reserved hardware, avoiding preemption.

---

## Conclusion

By containerizing your code and orchestration logic, Vertex AI Custom Jobs let you scale effortlessly to large GPU fleets, integrate with GCP’s IAM and monitoring, and reproduce experiments consistently. Once you’ve mastered this flow, you can:

* Add **distributed data pipelines** (Dataflow, BigQuery)
* Hook into **Hyperparameter Tuning** or **Vertex Vizier**
* Deploy your trained model with **Vertex Endpoints**

Happy scaling—and may your training queues always be short! 🚀
