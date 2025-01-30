def create_docker_compose():
    content = """
version: '3.8'
services:
  app:
    build: .
    container_name: my_app
    ports:
      - "8080:8080"
    """
    with open("data/temp_zip/docker-compose.yml", "w") as docker_compose:
        docker_compose.write(content)
    
    return "data/temp_zip/docker-compose.yml"