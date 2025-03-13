import subprocess
import requests
import os
import time

def test_zip(zip_path, uploaded_file_name):
    try:
        # Build the Docker containers
        subprocess.run(["docker", "rm", "flask-api"], cwd=zip_path)
        subprocess.run(["docker-compose", "up", "--build", "-d"], check=True, cwd=zip_path)

        time.sleep(1)  # Wait for the Flask API to start

        # Optional: Verify API response
        response = requests.post(url="http://localhost:9000/process", files={"file": open(os.path.join(zip_path, uploaded_file_name), "rb")})

        if response.status_code == 200:
            print("Flask API is running correctly!")
        else:
            print(f'Flask API returned {response.status_code}, check logs!')
        
        return True

    except subprocess.CalledProcessError as e:
        print(f'Error during Docker compose execution: {e}')
        return False
    finally:
        # Clean up after testing
        subprocess.run(["docker-compose", "down", "--rmi", "local"], cwd=zip_path)