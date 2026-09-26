# ---------- Stage 1: build dependencies ----------
FROM python:3.13.3-slim AS builder

# Copy uv from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv
RUN uv sync --frozen --no-install-project --no-dev


# ---------- Stage 2: runtime ----------
FROM python:3.13.3-slim

# Create a non-root user
RUN groupadd --system app && \
    useradd --system --gid app --create-home app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY --chown=app:app app/ ./app/

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]