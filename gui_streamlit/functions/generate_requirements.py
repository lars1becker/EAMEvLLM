import os
import subprocess

def generate_requirements(code_path):
    try:
        # Run pipreqs command to generate requirements.txt
        subprocess.run(['pipreqs', os.path.dirname(code_path), '--force', '--mode', 'no-pin'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error generating requirements: {e}')