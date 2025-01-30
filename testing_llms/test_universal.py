import ollama
import re
import pandas as pd
from huggingface_hub import InferenceClient
import time  # Import the time module
import subprocess
from dotenv import load_dotenv
import os
from pylint.lint import Run #Import the Run class from the pylint package
import psutil

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Test case names
test_case_names = ["image", "void", "page_rank", "connected_components"]

# Prompt for the test case
prompts = {
"image":
"""
You are an expert at programming python code. 
Write python code that extracts the file format, the image dimensions and the image aspect ratio of a given image-file. The image-file is stored at the path ./data/image/ocean.jpg. Store the result in a dictionary called result and print it at the end, like this (where the values are placeholders): 
```python
result = {
    'file_format': 'value',
    'dimensions': 'value',
    'aspect_ratio': 'value'
}
print(result)
```.
Just output the block of code without any additional text. Make sure the code works and compiles correctly.
""",
"void":
"""
You are an expert at programming python code. 
Write python code that extracts metadata from an RDF-File as specified in the VoID vocabulary, but only the predicate count and the class count
	1.	The predicate count: A count of all unique predicates in the RDF file.
	2.	The class count: A count of all unique RDF classes (i.e., objects of rdf:type triples).
The rdf file is stored at the path ./data/void/books.ttl. Store the result in a dictionary called result and print it at the end, like this (where the values are placeholders): 
```python
result = {
    'predicate_count': 'value',
    'class_count': 'value'
}
print(result)
```.
Just output the block of code without any additional text. Make sure the code works and compiles correctly.
""",
"page_rank":
"""
You are an expert at programming python code. 
Write python code that calculates the Page Rank scores for a given graph-file at the path ./data/page_rank/page_rank.gml. Store the result for each node in a dictionary called result and print it at the end, like this (where the values are placeholders): 
```python
result = {
    'A': 'value',
    'B': 'value',
    ...
}
print(result)
```.
Take the nodes as their labels and not their id.
Just output the block of code without any additional text. Make sure the code works and compiles correctly.
""",
"connected_components":
"""
You are an expert at programming python code. 
Write python code that calculates the connected components for a given graph-file at the path ./data/connected_components/connected_components.gml. It should calculate the strongly connected components as well as the weakly connected components. Store the result in a dictionary called result and print it at the end, like this (where the values are placeholders and A, B and so on are sample nodes): 
```python
result = {
    'strongly connected components count': 'value',
    'weakly connected components count': 'value',
    'strongly connected component 1': 'A, B, C',
    'strongly connected component 2': 'D, E',
    ...,
    'weakly connected component 1': 'A, B, C, F',
    'weakly connected component 2': 'D, E',
    ...,
}
print(result)
```.
Just output the block of code without any additional text. Make sure the code works and compiles correctly.
"""
}

# Models dictionary
models = {
    # "qwen2.5-coder": "qwen/qwen2.5-coder-32b-instruct",
    "llama3.2": "llama3.2:1b", 
    "codellama": "codellama:7b",
    "qwen2.5-coder": "qwen/qwen2.5-coder-32b-instruct"
}

# Define your general requirements and cases
requirements_map = {
    'image': {'file_format':'', 'dimensions':'', 'aspect_ratio':''},
    'void': {'predicate_count':'' , 'class_count':''},
    'page_rank': {'A':'', 'B':'', 'C':'', 'D':'', 'E':'', 'F':'', 'G':''},
    'connected_components': {
        'strongly connected components count': '',
        'weakly connected components count': '',
        'strongly connected component 1': '',
        'strongly connected component 2': '',
        'strongly connected component 3': '',
        'strongly connected component 4': '',
        'weakly connected component 1': '',
        'weakly connected component 2': ''
    }
}



# Select the test case 0 = image, 1 = void, 2 = page_rank, 3 = connected_components
test_case_name = test_case_names[3]

# Select the requirements for the test case
requirements = requirements_map[test_case_name]

# Select the prompt for the test case
prompt = prompts[test_case_name]

# Count of Iterations
iterations = 40



# Function to extract code from a response
def extract_code(response_text):
    # Use regex to extract text within code blocks (```)
    match = re.search(r"```(?:python)?\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the content inside the code block
    return response_text.strip()  # If no code block, return the raw response

# Function to generate text using Ollama
def generate_text_with_ollama(conversation, model):
    start_time = time.time()  # Record start time for LLM response generation
    response = ollama.chat(model=model, messages=conversation)
    end_time = time.time()  # Record end time for LLM response generation
    llm_runtime = end_time - start_time  # Calculate the runtime
    return response['message']['content'], llm_runtime

# Function to generate text using Cerebras
def generate_text_with_huggingface(conversation, model):
    start_time = time.time()  # Record start time for LLM response generation
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    messages = conversation

    completion = client.chat.completions.create(
        model=model, 
        messages=messages, 
        max_tokens=1500,
    )
    end_time = time.time()  # Record end time for LLM response generation
    llm_runtime = end_time - start_time  # Calculate the runtime
    return completion.choices[0].message.content, llm_runtime

def exec_code(model_name, iteration, revision, timeout=10):
    try:
        start_time = time.time()
        
        # Start the subprocess with a timeout
        process = subprocess.Popen(
            ["python", f"./data/{test_case_name}/code/{model_name}_{iteration}_{revision}.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        proc = psutil.Process(process.pid)
        memory_info = proc.memory_info()
        kb_memory_usage = memory_info.rss / 1024
        print(f'Memory Usage: {kb_memory_usage} KB')  # RSS (Resident Set Size)
        
        try:
            # Wait for the process to complete with a timeout
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # If the process exceeds the timeout, terminate it
            print(f"Process exceeded timeout of {timeout} seconds. Terminating...")
            process.terminate()
            try:
                process.wait(timeout=2)  # Wait briefly for graceful termination
                print("Subprocess terminated gracefully after timeout.")
            except subprocess.TimeoutExpired:
                print("Graceful termination failed. Forcing kill...")
                process.kill()
                process.wait()
                print("Subprocess killed.")
            return None, None, f"Process timed out after {timeout} seconds.", None

        # Stop the timer after code execution
        end_time = time.time()
        code_runtime = end_time - start_time

        # Access the standard output and error
        stdout = stdout.strip()
        stderr = stderr.strip()

        if stderr:
            print(f"Standard Error:\n{stderr.splitlines()[-1]}")

        # Attempt to extract a dictionary from stdout
        match = re.search(r"\{.*?\}", stdout, re.DOTALL)
        if match:
            # Parse the matched dictionary string safely
            extracted_dict = eval(match.group(0))
            if isinstance(extracted_dict, dict):
                print(f"Extracted Dictionary: {extracted_dict}")
                return extracted_dict, code_runtime, None, kb_memory_usage  # Return the dictionary if valid
            else:
                print(f"Output is not a valid dictionary: {stdout}")
                if not stderr:
                    return None, code_runtime, 'No dictionary found! ' + stdout, kb_memory_usage
                else:
                    return None, None, stderr, None
        else:
            print(f"No dictionary found in output. Stdout: {stdout}")
            if not stderr:
                return None, code_runtime, 'No dictionary found! ' + stdout, kb_memory_usage
            else:
                return None, None, stderr, None

    except Exception as e:
        # Handle unexpected execution errors
        print(f"Exception occurred during execution: {e}")
        return None, None, e, None

# Initialize a list to hold the data for the CSV
results_list = []

# Make sure the directories are setup
os.makedirs(f"data", exist_ok=True)
for test_case in test_case_names:
    for folder in ["code", "output"]:
        os.makedirs(f"data/{test_case}/{folder}", exist_ok=True)

# Clear output files for each model
for model_name in models:
    with open(f"data/{test_case_name}/output/" + model_name + ".txt", "w") as f:
        pass

# Main loop to iterate over models and prompt generation
for model_name, selected_model in models.items():
    for i in range(iterations):
        # Initialize a dictionary to hold the conversation history for revision
        conversation = [
            {"role": "user", "content": prompt}
        ]

        for j in range(3):
            print(f"Model: {model_name}, Iteration: {i + 1}, {'Revision ' + str(j) if j != 0 else ''}")

            # Generate text and code with the selected model
            if model_name == "qwen2.5-coder":
                response, llm_runtime = generate_text_with_huggingface(conversation, selected_model)
            else:
                response, llm_runtime = generate_text_with_ollama(conversation, selected_model)

            conversation.append({"role": "assistant", "content": response})

            code = extract_code(response)

            # Save the code to a file
            with open(f"data/{test_case_name}/code/{model_name}_{i + 1}_{j}.py", "w") as f:
                f.write(code)

            # Run pylint and capture the output
            results = Run(args=[
                f"data/{test_case_name}/code/{model_name}_{i + 1}_{j}.py"
                ], exit=False)
            score = results.linter.stats.global_note  # Get the score from linter stats

        
            # Execute the code and capture the result
            exec_result, code_runtime, error, memory_usage = exec_code(model_name, i + 1, j)
            if code_runtime is not None:
                break
            else:
                conversation.append({"role": "user", "content": f"The code execution failed. Please revise the code using the error: {error}"})

        # After normalizing, assign values to the requirements
        if isinstance(exec_result, dict):
            for req in requirements:
                requirements[req] = exec_result.get(req)
        else:
            for req in requirements:
                requirements[req] = None

        try:
            error_message = error.splitlines()[-1] if error and hasattr(error, "splitlines") else None
        except (AttributeError, IndexError):
            error_message = None

        # Append the results to the list for CSV export
        results_list.append({
            "Model": model_name,
            "Iteration": i + 1,
            "Revisions": j,
            "LLM_Response_Time (s)": llm_runtime,
            **{req: requirements[req] for req in requirements}, 
            "Error": error_message,
            "Code_Execution_Time (s)": code_runtime,
            "Memory_Usage (KB)": memory_usage,
            "Pylint_Score (0-10)": score,
        })

        # Save runtime data to the text file
        with open(f"data/{test_case_name}/output/" + model_name + ".txt", "a") as f:
            f.write(f"Iteration {i + 1}: {'Revision ' + str(j) if j != 0 else ''}\n")
            if code_runtime is not None:
                f.write(f"LLM Response Time: {llm_runtime:.4f} sec, Code Execution Time: {code_runtime:.4f} sec, Memory Usage: {memory_usage:.2f} KB, PyLint Score: {score:.2f}\n")
                for req in requirements:
                    f.write(f"{req}: {requirements[req]} ")
                f.write("\n")
            else:
                f.write(f"LLM Response Time: {llm_runtime:.4f} sec, Code Execution failed\n")
                f.write(f"Error: {error_message}\n")
            f.write("\n")

# Create a DataFrame from the results list and save it to a CSV
results_df = pd.DataFrame(results_list)
results_df.to_csv(f"data/{test_case_name}/code_execution_results.csv", index=False)
print("Results saved to data/code_execution_results.csv")