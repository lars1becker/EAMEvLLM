def create_readme():
    content = """
# My App
docker and docker-compose needs to be installed

In terminal run the following command:
docker-compose up --build

The API enpoint is available at:
http://localhost:9000/process?path=file://path/to/file

Testing via:
curl "http://localhost:9000/process?path=file://path/to/file"

    """
    with open("data/temp_zip/README.md", "w") as readme:
        readme.write(content)

    return "data/temp_zip/README.md"