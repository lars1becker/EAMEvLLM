import sys

def extract_requirements_pip(code):
    # Extract the requirements from the code
    requirements = []
    for line in code.split("\n"):
        if "import" in line:
            libraries = sys.stdlib_module_names
            library = line.split(" ")[1].split(".")[0]
            if library not in libraries:
                requirements.append(library)
    return requirements

def create_requirements(coding_language, code):
    # Python script to create a requirements file
    if coding_language == "python":
        extracted_requirements = extract_requirements_pip(code)
    else:
        extracted_requirements = []

    with open("data/temp_zip/requirements.txt", "w") as requirements:
        # Add Flask for API deployment
        requirements.write("Flask\n")
        for requirement in extracted_requirements:
            requirements.write(requirement + "\n")
            
    return "data/temp_zip/requirements.txt"
