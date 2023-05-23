# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Apache Pulsar client library
RUN pip install -r requirements.txt

# Copy the Python script to the working directory
COPY producer.py .

# Expose the necessary port(s) for Pulsar communication
EXPOSE 6650

# Set the command to run your Python script
CMD ["python", "producer.py"]
