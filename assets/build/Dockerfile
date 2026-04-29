# =============================================================
# Unified Dockerfile for gabriel-navarro-bio
#
# Build a target with:
#   docker build --target dev  -t app:dev  -f assets/build/Dockerfile .
#   docker build --target prod -t app:prod -f assets/build/Dockerfile .
#
# Packages are installed via `pip install --prefix=/install` in a
# builder stage and then COPY'd into /usr/local in the runtime
# stages. This puts them in Python's default search path
# (/usr/local/lib/python3.13/site-packages), so no venv or PATH
# manipulation is needed for site-packages.
#
# Source of truth for dependencies: pyproject.toml (no requirements
# files; legacy requirements.{prod,dev}.txt were removed in Epic D's
# pyproject migration).
# =============================================================


# -------------------------------------------------------------
# STAGE 1: prod-builder — compile production deps into /install
# -------------------------------------------------------------
FROM python:3.13-alpine AS prod-builder

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        python3-dev

# Copy only the metadata needed to resolve runtime deps. The src/
# tree is copied so the editable install can find the package layout.
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install . && \
    find /install -type d -name __pycache__ -exec rm -rf {} + && \
    find /install -name "*.py[co]" -delete && \
    apk del .build-deps


# -------------------------------------------------------------
# STAGE 2: dev-builder — layer dev deps on top of prod deps
# -------------------------------------------------------------
FROM prod-builder AS dev-builder

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        python3-dev

# Re-install with [dev] extras to pull in pytest, ruff, mypy, etc.
RUN pip install --no-cache-dir --prefix=/install ".[dev]" && \
    apk del .build-deps


# -------------------------------------------------------------
# STAGE 3: dev — development runtime with tooling
# -------------------------------------------------------------
FROM python:3.13-alpine AS dev

WORKDIR /app

# Developer tooling: shell, VCS, network, GitHub CLI, Node (for
# Claude Code), and the Google Cloud SDK for local auth against
# GCP services.
RUN apk add --no-cache \
        bash \
        git \
        curl \
        wget \
        github-cli \
        nodejs \
        npm && \
    npm install -g @anthropic-ai/claude-code && \
    curl -sSL https://sdk.cloud.google.com | bash

# Put gcloud on PATH so `gcloud`, `gsutil`, `bq`, etc. work without
# the full `/root/google-cloud-sdk/bin/...` prefix in any shell.
ENV PATH="/root/google-cloud-sdk/bin:${PATH}"

# Pull in prod + dev Python packages staged by dev-builder.
COPY --from=dev-builder /install /usr/local

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


# -------------------------------------------------------------
# STAGE 4: prod — minimal runtime image (default build target)
# -------------------------------------------------------------
FROM python:3.13-alpine AS prod

WORKDIR /app

COPY --from=prod-builder /install /usr/local
COPY app.py /app/app.py
COPY src /app/src
COPY assets/ico/favicon.ico /app/assets/ico/favicon.ico

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 80

CMD ["python", "/app/app.py"]
