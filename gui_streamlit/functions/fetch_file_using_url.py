import requests
from io import BytesIO

def fetch_file_using_url(file_url, max_size):
    # Fetch file from URL
    response = requests.get(file_url, stream=True)
    response.raise_for_status()  # Raise an error for HTTP issues
    # Check if the file size exceeds the maximum allowed size
    if int(response.headers.get("Content-Length", 0)) > max_size:
        return None, f'File exceeds the maximum allowed size of {max_size / 1024 / 1024}MB.'
    else:
        file = BytesIO(response.content)
        file.name = file_url.split("/")[-1]  # Set a name for the file
        return file, None