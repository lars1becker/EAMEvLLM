import subprocess

def exec_code(timeout=10, coding_language="python"):
    try:
        # Start the subprocess with a timeout
        process = subprocess.Popen(
            [f"{coding_language}", f"./data/code.py" if coding_language == "python" else f"./data/code.java"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Wait for the process to complete with a timeout
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # If the process exceeds the timeout, terminate it
            process.terminate()
            try:
                process.wait(timeout=2)  # Wait briefly for graceful termination
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            return f"Process timed out after {timeout} seconds."

        # Access the standard output and error
        stdout = stdout.strip()
        stderr = stderr.strip()

        if stderr:
            return f"Standard Error:\n{stderr.splitlines()[-1]}"
        else:
            return stdout
    except Exception as e:
        # Return the exception message if an error occurs
        return f"Exception occurred during execution: {e}"