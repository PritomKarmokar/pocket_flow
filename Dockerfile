# =========================
# 🏗️ Builder Stage
# =========================
FROM python:3.13-slim AS builder

# Create and set working directory
# (WORKDIR will create /app automatically, so mkdir is optional)
RUN mkdir /app
WORKDIR /app

# Python environment variables:
# - Prevents Python from writing .pyc files (keeps container clean)
# - Ensures logs are printed directly (useful for Docker logs)
# - Disables pip cache (reduces image size)
# - Disables pip version check (faster builds)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
# build-essential → for compiling packages (C extensions)
# libpq-dev → required for PostgreSQL (psycopg2)
# Remove apt cache to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (important for Docker caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
# Done in builder stage so final image stays small
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# =========================
# 🚀 Final Stage (Runtime)
# =========================
FROM python:3.13-slim

# Create a non-root user for security
# Running as root in containers is risky
RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy installed Python packages from builder stage
# This avoids reinstalling dependencies in final image
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/

# Copy executables (like gunicorn) from builder
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory inside container
WORKDIR /app

# Copy entire project code into container
# --chown ensures appuser owns the files (avoids permission issues)
COPY --chown=appuser:appuser . .

# Python runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

RUN chmod +x /app/entrypoint.sh /app/start.sh

# Docker Run Checks and Configurations
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["/app/start.sh", "server"]