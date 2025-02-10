# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install Node.js, npm, and Sass (SCSS) support
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends nodejs npm && \
#    npm install -g sass && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*


# ✅ Force install MySQL client
RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*



# Set working directory in container
WORKDIR /app




# Copy requirements file
COPY app_data/requirements2.txt .


# ✅ Ensure `PYTHONPATH` includes `/app`
ENV PYTHONPATH="/app"


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements2.txt

# Copy app files
COPY app_data/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

COPY app_data/ /app

# Compile Sass to CSS
#RUN mkdir -p source output && \
#    echo '$bg-color: #333;' > source/styles.scss && \
#    echo 'body { background-color: $bg-color; }' >> source/styles.scss && \
#    sass source/styles.scss output/styles.css

# Specify the command to run on container start
CMD ["sh", "-c", "/app/wait-for-it.sh phishing-scan-platform-db 3306 -- python app.py"]
