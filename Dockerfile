# Multi-stage build for optimized production Docker image
# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="ACEest DevOps Team"
LABEL description="ACEest Fitness & Gym - Flask REST API"
LABEL version="1.0.0"

# Set environment variables
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

# Create non-root user for security
RUN useradd -m -u 1000 aceest && \
    mkdir -p /app && \
    chown -R aceest:aceest /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder --chown=aceest:aceest /root/.local /home/aceest/.local

# Copy application code
COPY --chown=aceest:aceest app.py .
COPY --chown=aceest:aceest requirements.txt .

# Update PATH for pip user install
ENV PATH=/home/aceest/.local/bin:$PATH

# Switch to non-root user
USER aceest

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
