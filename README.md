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
Authenticate with Google Cloud:
```bash
gcloud auth login
```
Configure Docker to use Google Cloud:
```bash
gcloud auth configure-docker
```

Build and tag the image:
```bash
# Build the Docker image for production
docker build -f ./assets/build/Dockerfile.prod -t gnbio:prod .
# Tag the image for Google Container Registry
docker tag gnbio:prod us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod
```

Push the image to Google Container Registry:
```bash
docker push us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod
```

Deploy to Cloud Run:
```bash
gcloud run deploy gabriel-navarro-bio \
  --image gcr.io/YOUR_PROJECT_ID/gabriel-navarro-bio \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1
```

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

