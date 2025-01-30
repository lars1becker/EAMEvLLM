def create_dockerfile(coding_language):
    # Python script to create a Dockerfile
    dockerfile_content_dict = {
        "python" : 
        """
# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY code.py .

# Command to run the Python script
CMD ["python", "code.py"]
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