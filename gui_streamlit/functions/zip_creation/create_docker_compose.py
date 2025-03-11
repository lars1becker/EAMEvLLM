def create_docker_compose(temp_path):
    content = """
version: '3.8'
services:
  flask-api:
    build: .
    image: flask-api
    container_name: flask-api
    ports:
      - "9000:9000"  # Change if your Flask app runs on a different port
    restart: unless-stopped
    """
    with open(f'{temp_path}/docker-compose.yml', "w") as docker_compose:
        docker_compose.write(content)
    
    return f'{temp_path}/docker-compose.yml'