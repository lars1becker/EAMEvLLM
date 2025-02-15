import os
import shutil

from functions.zip_creation.create_api_app import create_api_app
from functions.zip_creation.create_docker_compose import create_docker_compose
from functions.zip_creation.create_dockerfile import create_dockerfile
from functions.zip_creation.create_readme import create_readme
from functions.generate_requirements import generate_requirements

def create_zip(code_path, data_files):
    TEMP_PATH = "temp/zip"

    # Create the temp path if it doesn't exist
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
    # Clear the temp path excluding the code file
    for file in os.listdir(TEMP_PATH):
        if file != os.path.basename(code_path):
            os.remove(os.path.join(TEMP_PATH, file))

    # Create the necessary files for the ZIP file
    api_app_path = create_api_app(TEMP_PATH)
    docker_compose_path = create_docker_compose(TEMP_PATH)
    dockerfile_path = create_dockerfile(TEMP_PATH)
    readme_path = create_readme(TEMP_PATH)

    # Generate requirements.txt
    generate_requirements(code_path)

    # Copy the data files to the temp path
    for data_file in data_files:
        shutil.copy(data_file, TEMP_PATH)

    # Files to be zipped
    files_to_zip = [code_path, api_app_path, docker_compose_path, dockerfile_path, readme_path]

    # Ensure all necessary files exist
    for file in files_to_zip:
        if not os.path.exists(file):
            return f"Failed to generate {file}."

    # Create a ZIP file
    shutil.make_archive("temp/output", "zip", TEMP_PATH)

    return "temp/output.zip"