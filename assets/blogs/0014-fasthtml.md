@{id = "cfe27c28-2686-4ed6-88b4-f9563df532d5"
  title = "Web Development with FastHTML"
  date = "2025-04-27T00:00:00Z"
  tags = ['docker', 'webdevelopment', 'html']
  views = 0
  likes = 0
  image = "https://storage.googleapis.com/gn-portfolio/images/fasthtml-thumb.svg"
  description = "COMING SOON"
  type = "note"
  disabled = "true"
}
# TODO: COMPLETE Web Development with FastHTML

# Getting Started with FastHTML in Docker

**FastHTML** is a next-generation Python web framework built around HTMX, letting you write ultra-light, interactive web apps with minimal boilerplate. In this tutorial, you’ll learn how to:

1. Install FastHTML via **pip**
2. Containerize your app with **Docker**
3. Run a simple “Hello World” example with HTMX interactivity

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing FastHTML](#installing-fasthtml)
3. [Writing Your First FastHTML App](#writing-your-first-fasthtml-app)
4. [Dockerizing Your App](#dockerizing-your-app)
5. [Building & Running the Container](#building--running-the-container)
6. [Example: Click-to-Change Text](#example-click-to-change-text)
7. [Next Steps & Resources](#next-steps--resources)

---

## Prerequisites

- **Python 3.8+**
- **Docker** v20.10+ (with daemon running)
- Familiarity with the command line

---

## Installing FastHTML

First, install FastHTML into a local virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install python-fasthtml

Tip: FastHTML uses HTMX under the hood—no extra JavaScript is required!

⸻

Writing Your First FastHTML App

Create a file main.py:

# main.py
from fasthtml.common import *

app, rt = fast_app()

# Root route: “Hello World!”
@rt('/')
def get_root():
    return Div(
        P('Hello World!', id='greeting'),
        HxButton('Change Text', hx_get='/change')
    )

# HTMX endpoint: replace paragraph text
@rt('/change')
def get_change():
    return P('Nice to be here!', id='greeting')

if __name__ == '__main__':
    serve()  # starts on http://localhost:5001

	•	fast_app() sets up the FastHTML/HTMX runtime.
	•	HxButton generates <button hx-get="…"> for click-driven partial updates.
	•	serve() launches the built-in development server.

Run locally:

python main.py

Open http://localhost:5001 in your browser and click “Change Text.”

⸻

Dockerizing Your App

Create a Dockerfile next to main.py:

# Use a slim Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY main.py .

# Expose default FastHTML port
EXPOSE 5001

# Run the app
CMD ["python", "main.py"]

And a requirements.txt:

python-fasthtml



⸻

Building & Running the Container

Build the image:

docker build -t fasthtml-app .

Run the container:

docker run --rm -p 5001:5001 fasthtml-app

Now navigate to http://localhost:5001 and interact with your FastHTML app inside Docker!

⸻

Example: Click-to-Change Text
	1.	Visit your app at http://localhost:5001.
	2.	Click the “Change Text” button.
	3.	Observe the <p> element update from “Hello World!” to “Nice to be here!” without a full page reload.

This HTML-over-the-wire approach, powered by HTMX and FastHTML, keeps your Python code concise and your user experience snappy.

⸻

Next Steps & Resources
	•	Deep Dive: Read the FastHTML About page for design philosophy.
	•	Examples: Browse the FastHTML Examples Repo.
	•	Community: Join the FastHTML Discord to ask questions and share projects.
	•	Advanced Features: Learn about WebSocket support, database integration, and custom components in the official docs.

Happy coding with FastHTML! 🚀
