FROM python:3.10.6-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image.
COPY requirements.txt ./

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . .

# Run the Python script on container startup.
CMD ["python", "appsflyer-test.py"]
