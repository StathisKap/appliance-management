# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache /wheels/*

# Copy project files
COPY . .

# Ensure proper permissions
RUN mkdir -p /app/staticfiles && \
    chmod -R 755 /app && \
    chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint to run migrations and collectstatic before starting Gunicorn
ENTRYPOINT ["./entrypoint.sh"]

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app_manager.wsgi:application"]
