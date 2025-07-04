# NOFACE.digital Bot - Professional Docker Image
# Multi-stage build for production optimization

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r botuser && useradd -r -g botuser botuser

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/botuser/.local

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Make sure scripts in .local are usable
ENV PATH=/home/botuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port (if needed for webhooks)
EXPOSE 8080

# Set default environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"] 