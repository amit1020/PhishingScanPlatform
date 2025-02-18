# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install MySQL client and netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

COPY ./app_data/Keys/ /app/Keys/

# Copy requirements and install dependencies
COPY ./app_data/requirements2.txt .
ENV PYTHONPATH="/app"
RUN pip install --no-cache-dir -r requirements2.txt

# Copy application files
COPY ./app_data/wait-for-connection.sh /app/wait-for-connection.sh
RUN chmod +x /app/wait-for-connection.sh

COPY ./app_data/ /app

# Run the application
CMD ["sh", "-c", "/app/wait-for-connection.sh phishing-scan-platform-db 3306 -- python app.py"]
