def create_dockerfile(coding_language):
    # Python script to create a Dockerfile
    dockerfile_content_dict = {
        "python" : 
        """
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
        """,
        "java" : 
        """
# Use an official OpenJDK runtime as a base image
FROM openjdk

WORKDIR /app

COPY . /app

RUN javac Code.java

CMD ["java","Code"]
        """
    }

    dockerfile_content = dockerfile_content_dict[coding_language]

    # Write the content to a Dockerfile
    with open("data/temp_zip/Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    return "data/temp_zip/Dockerfile"