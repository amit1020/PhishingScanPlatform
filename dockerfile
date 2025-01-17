# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install Node.js, npm and Sass (SCSS) support
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g sass && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app_data/requirements2.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements2.txt

# Copy the rest of the application code into the container
COPY app_data/ .

# Ensure the source directory exists and compile Sass to CSS
RUN mkdir -p source output && \
    echo '$bg-color: #333;' > source/styles.scss && \
    echo 'body { background-color: $bg-color; }' >> source/styles.scss && \
    sass source/styles.scss output/styles.css

# Specify the command to run on container start
CMD [ "python", "app.py" ]
