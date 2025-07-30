FROM python:3.13.5-slim-bookworm

ARG VERSION

# Install uv for faster package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install pyatlan from PyPI
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache-dir pyatlan==${VERSION}

# Set working directory
WORKDIR /app

CMD ["python"]
