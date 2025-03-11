def create_dockerfile(temp_path):
    # Python script to create a Dockerfile
    dockerfile_content= """
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app on port 9000
EXPOSE 9000

# Run the Flask app when the container starts
CMD ["python", "app.py"]
"""

    # Write the content to a Dockerfile
    with open(f'{temp_path}/Dockerfile', "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    return f'{temp_path}/Dockerfile'