# gabriel-navarro-bio
Bio webpage for a modern, Python-based portfolio website built with FastHTML and deployed on Google Cloud Run using Uvicorn.


## 🚀 Overview
This repository contains code for a personal portfolio website built with FastHTML - a Python library that provides a 1:1 mapping to HTML and HTTP, allowing for powerful web development using Python's full ecosystem. The application is designed to be deployed on Google Cloud Run for scalable, serverless hosting with minimal configuration.


### ✨ Features
* Python-First Development: Leverage the full power of Python for building a modern portfolio website
* Simple Deployment: Optimized for Google Cloud Run's serverless architecture
* High Performance: Uses Uvicorn ASGI server for fast, efficient request handling
* Developer Friendly: Clean codebase with best practices for maintainability
* Responsive Design: Mobile-first approach for a great experience on all devices


### 🛠️ Tech Stack
* FastHTML: Python library that maps directly to HTML and HTTP
* Uvicorn: Lightning-fast ASGI server implementation
* Google Cloud Run: Fully managed serverless platform
* Docker: Containerization for consistent deployment
* GitHub Actions: CI/CD pipeline for automated deployment (optional)


### 📋 Prerequisites
* Python 3.11+
* Docker (for local testing and deployment)
* Google Cloud account
* Google Cloud CLI (for deployment)


## 🚦 Getting Started
### Installation
1. Clone this repository:
```bash
git clone https://github.com/gabenavarro/gabriel-navarro-bio.git
cd gabriel-navarro-bio
```


### Local Development
1. Setup local envrionment and install dependencies:
```bash
docker build -f ./assets/build/Dockerfile.dev -t gnbio:local .
```

2. Run docker environment
Run the application locally using Uvicorn:
```bash
docker run -dt \
  -p 8080:8080 \
  --env GOOGLE_APPLICATION_CREDENTIALS="/app/assets/secrets/gcp_credentials.json" \
  --env GOOGLE_CLOUD_CREDENTIALS="/app/assets/secrets/gcp_credentials.json" \
  -v $(pwd)/:/app/ \
  --name gnbio \
  gnbio:local
```

3. Attach container to vscode or your favorite IDE.

3. Run uvicorn in IDE container
```bash
python /app/app.py --port 8080
```

The site will be available at http://localhost:8080.


### 🚢 Deployment to Google Cloud Run

**Pushes to `main` automatically deploy to Cloud Run** via the [`Deploy to Cloud Run`](.github/workflows/deploy.yml) workflow:
1. Run lint + tests (must pass)
2. Build Docker image from `assets/build/Dockerfile.prod`
3. Push to Artifact Registry tagged both `:prod` and `:sha-<short-sha>`
4. Deploy to the `gnbio` Cloud Run service in `us-central1`

The workflow authenticates to GCP via Workload Identity Federation (no long-lived JSON keys).

#### Manual deploy (rollback or local testing)

```bash
# Authenticate and configure Docker
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and tag
docker build -f ./assets/build/Dockerfile.prod \
  -t us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod .

# Push and deploy
docker push us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod
gcloud run deploy gnbio \
  --image us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod \
  --platform managed \
  --region us-central1
```

#### Rolling back

Each automated deploy tags the image with the commit SHA. To roll back:

```bash
# Pick a known-good <short-sha> from `git log` or the GH Actions run history
gcloud run deploy gnbio \
  --image us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:sha-<short-sha> \
  --region us-central1
```

## CLI

The `src.cli` module provides operations for managing blog posts.

```bash
# Validate a markdown file's frontmatter
python -m src.cli blog validate assets/blogs/0001-fastp.md

# Submit a new post to BigQuery (dry-run prints the payload)
python -m src.cli blog submit assets/blogs/0001-fastp.md --dry-run
python -m src.cli blog submit assets/blogs/0001-fastp.md

# Upsert an existing post (delete-then-insert by id)
python -m src.cli blog update assets/blogs/0001-fastp.md --dry-run

# Mark a post as disabled (hides from /blogs)
python -m src.cli blog disable <uuid>

# List posts
python -m src.cli blog list           # active only
python -m src.cli blog list --all     # include disabled
```

Requires `GOOGLE_APPLICATION_CREDENTIALS` env var pointing at a service-account JSON
for any command that touches BigQuery (submit, update, disable, list).

## 📁 Code Structure

The project follows a feature-based architecture optimized for FastHTML and MonsterUI, designed to be highly maintainable and LLM-friendly.

```txt
src/
├── config/             # Centralized settings and constants
├── core/               # App factory and route registration
├── styles/             # Consolidated CSS and theme definitions
├── components/         # Reusable UI components
│   ├── base/           # Icons, buttons, chips
│   ├── layout/         # High-level page structures and navigation
│   ├── decorative/     # Backgrounds and parallax effects
│   └── modals/         # Functional modal components
├── features/           # Feature-specific page logic and components
│   ├── hero/           # Landing page landing
│   ├── projects/       # Portfolio and blog systems
│   └── cv/             # Resume/CV page
├── services/           # External integrations (GCP, JS interop)
├── models/             # Shared data structures
└── utils/              # General helper functions
```
