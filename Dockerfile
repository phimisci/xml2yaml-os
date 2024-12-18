# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set ENV variables (used in the script to set the correct path)
ENV IS_CONTAINER=true

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "xml2yaml.py"]
