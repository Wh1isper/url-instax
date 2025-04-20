FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

RUN apt-get update && apt-get install -y tini && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
COPY uv.lock /app/uv.lock
COPY pyproject.toml /app/pyproject.toml

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project
RUN uv sync --frozen

EXPOSE 8890
ENTRYPOINT [ "tini", "--", "uv", "run", "url-instax"]
CMD ["http"]
