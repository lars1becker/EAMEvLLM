# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app on port 5000
EXPOSE 5000

# Run the Flask app when the container starts
CMD ["python", "app.py"]