# Use Python 3.12.3 as base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Set Python-specific environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for psycopg2-binary
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/
COPY entrypoint.sh /app/
# Convert line endings and set permissions
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Expose the port from environment (default to 8000 if not set)
EXPOSE ${PORT:-8000}

# Use entrypoint script to start the application
ENTRYPOINT ["/app/entrypoint.sh"]