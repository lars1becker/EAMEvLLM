def create_readme():
    content = """
# My App
docker and docker-compose needs to be installed

In terminal run the following command:
docker-compose up --build

    """
    with open("data/temp_zip/README.md", "w") as readme:
        readme.write(content)

    return "data/temp_zip/README.md"