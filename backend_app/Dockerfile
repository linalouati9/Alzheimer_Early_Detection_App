# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files to the container
COPY ./script.py ./app.py ./requirements.txt ./best_model.tflite /app/

# Install system dependencies and clean up
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose required ports
EXPOSE 5000 8888

# Default command to run the Flask app
CMD ["python", "app.py"]
