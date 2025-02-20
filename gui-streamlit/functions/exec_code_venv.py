import subprocess
import os
import sys
import tempfile
import shutil
import time
import psutil

from functions.generate_requirements import generate_requirements

def create_virtual_env(env_path):
    """Creates a virtual environment at the specified path."""
    subprocess.run([sys.executable, "-m", "venv", env_path], check=True)

def install_dependencies(env_path, code_path):
    """Installs required dependencies inside the virtual environment."""
    with open(os.path.dirname(code_path) + "/requirements.txt", "r") as file:
        requirements = file.read().splitlines()
    pip_executable = os.path.join(env_path, "bin", "pip") if os.name != "nt" else os.path.join(env_path, "Scripts", "pip.exe")
    for requirement in requirements:
        if requirement != "":
            subprocess.run([pip_executable, "install", requirement], check=True)

def execute_in_virtual_env(env_path, code_path, uploaded_file_path, timeout):
    """Executes the given Python code inside the virtual environment with runtime and memory tracking."""
    python_executable = os.path.join(env_path, "bin", "python") if os.name != "nt" else os.path.join(env_path, "Scripts", "python.exe")

    process = None
    try:
        start_time = time.time()

        process = subprocess.Popen(
            [python_executable, code_path, uploaded_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor resource usage
        ps_process = psutil.Process(process.pid)
        max_memory_usage = 0

        while process.poll() is None and time.time() - start_time < timeout/2:
            max_memory_usage = max(max_memory_usage, ps_process.memory_info().rss)  # Memory in bytes
            time.sleep(0.1)

        stdout, stderr = process.communicate(timeout=timeout/2)

        end_time = time.time()
        runtime = end_time - start_time

        return stdout, stderr, f"{runtime:.2f}", f"{max_memory_usage / (1024 * 1024):.2f}"  # Convert bytes to MB
    except subprocess.TimeoutExpired:
        if process:
            process.kill()
        return None, "Execution timed out after {} seconds.".format(timeout), None, None
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, None, None
    finally:
        if process:
            process.kill()

def exec_code_venv(code_path, uploaded_file_path, timeout):
    """Executes user-provided code in an isolated environment with resource tracking."""
    env_dir = tempfile.mkdtemp()
    
    try:
        create_virtual_env(env_dir)
        generate_requirements(code_path)
        install_dependencies(env_dir, code_path)
        output, error, runtime, memory_usage = execute_in_virtual_env(env_dir, code_path, uploaded_file_path, timeout)

        if error:
            return f"Standard Error:\n{error}", None, None
        else:
            return output, runtime, memory_usage
    finally:
        shutil.rmtree(env_dir)