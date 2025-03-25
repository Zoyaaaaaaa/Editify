# Use Python 3.12 as the base image
FROM python:3.12-slim

# Install system dependencies (required for OpenCV)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the Flask port (default: 5000)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]