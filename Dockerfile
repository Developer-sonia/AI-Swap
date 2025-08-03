# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create necessary directories
RUN mkdir -p backend/uploads backend/results backend/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=backend.wsgi

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--config", "backend/gunicorn.conf.py", "backend.wsgi:app"] 