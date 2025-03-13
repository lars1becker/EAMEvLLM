def create_readme(temp_path):
    content = """
# Metadata Extraction API
docker and docker-compose needs to be installed

In terminal run the following command:
docker-compose up --build

The API enpoint is available at:
http://localhost:9000/process

Testing via:
curl -X POST -F "file=@/path/to/file" "http://localhost:9000/process"

Using the batch script (with a directory containing files):
1. chmod +x run_metadata_extraction.sh
2. ./run_metadata_extraction.sh /path/to/directory
    """
    with open(f'{temp_path}/README.md', "w") as readme:
        readme.write(content)

    return f'{temp_path}/README.md'