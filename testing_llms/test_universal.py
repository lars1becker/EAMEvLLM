import ollama
import re
import pandas as pd
from huggingface_hub import InferenceClient
import time  # Import the time module
import subprocess
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Test case name
test_case_name = "image"

# Prompt for the test case
prompts = {
"image":
"""
You are an expert at programming python code. 
Write python code that extracts the file format, the image dimensions and the image aspect ratio of a given image-file. The image-file is stored at the path ./data/image/ocean.jpg. Save the result to a dictonary called result and print out at the end, like this (where the values are placeholders): 
```python
result = {
    'file_format': 'value',
    'dimensions': 'value',
    'aspect_ratio': 'value'
}
print(result)
```.
Just give the code block as output without any additional text. Make sure the code works correctly and compiles.
""",
"void":
"""
You are an expert at programming python code. 
Write python code that extracts the VoID-Statistics, namely predicate count and class count from a given rdf file in format of Turtle. The rdf file is stored at the path ./data/void/input.ttl. Save the result to a dictonary called result and print out at the end, like this (where the values are placeholders): 
```python
result = {
    'predicate_count': 'value',
    'class_count': 'value'
}
print(result)
```.
Just give the code block as output without any additional text. Make sure the code works correctly and compiles.
"""
}

# Models dictionary
models = {"llama3.2": "llama3.2:1b", "codellama": "codellama:7b", "qwen2.5-coder": "qwen/qwen2.5-coder-32b-instruct"}

# Define your general requirements and cases
requirements_map = {
    'image': {'file_format':'', 'dimensions':'', 'aspect_ratio':''},
    'void': {'predicate_count':'' , 'class_count':''}
}

requirements = requirements_map[test_case_name]

prompt = prompts[test_case_name]



# Function to extract code from a response
def extract_code(response_text):
    # Use regex to extract text within code blocks (```)
    match = re.search(r"```(?:python)?\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the content inside the code block
    return response_text.strip()  # If no code block, return the raw response

# Function to generate text using Ollama
def generate_text_with_ollama(prompt, model):
    start_time = time.time()  # Record start time for LLM response generation
    response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    end_time = time.time()  # Record end time for LLM response generation
    llm_runtime = end_time - start_time  # Calculate the runtime
    return response['message']['content'], llm_runtime

# Function to generate text using Cerebras
def generate_text_with_huggingface(prompt, model):
    start_time = time.time()  # Record start time for LLM response generation
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model=model, 
        messages=messages, 
        max_tokens=1500,
    )
    end_time = time.time()  # Record end time for LLM response generation
    llm_runtime = end_time - start_time  # Calculate the runtime
    return completion.choices[0].message.content, llm_runtime
    
def exec_code(model_name, iteration):
    try:
        start_time = time.time()
        
        # Execute the code
        result = subprocess.run(
            ["python", f"./data/{test_case_name}/code/{model_name}_{iteration}.py"],
            capture_output=True,
            text=True
        )
        
        # Stop the timer after code execution
        end_time = time.time()
        code_runtime = end_time - start_time  # Calculate runtime

        # Access the standard output and error
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stderr:
            print(f"Standard Error:\n{stderr.splitlines()[-1]}")

        # Attempt to extract a dictionary from stdout
        match = re.search(r"\{.*?\}", stdout, re.DOTALL)
        if match:
            # Parse the matched dictionary string safely
            extracted_dict = eval(match.group(0))
            if isinstance(extracted_dict, dict):
                print(f"Extracted Dictionary: {extracted_dict}")
                return extracted_dict, code_runtime, None  # Return the dictionary if valid
            else:
                print(f"Output is not a valid dictionary: {stdout}")
                if not stderr:
                    return None, None, 'No dictionary found! ' + stdout
                else:
                    return None, None, stderr.splitlines()[-1]
        else:
            print(f"No dictionary found in output. Stdout: {stdout}")
            if not stderr:
                return None, None, 'No dictionary found! ' + stdout
            else:
                return None, None, stderr.splitlines()[-1]
    except Exception as e:
        # Handle unexpected execution errors
        print(f"Exception occurred during execution: {e}")
        return None, None, e

# Initialize a list to hold the data for the CSV
results_list = []

# Clear output files for each model
for model_name in models:
    with open(f"data/{test_case_name}/output/" + model_name + ".txt", "w") as f:
        pass

# Main loop to iterate over models and prompt generation
for model_name, selected_model in models.items():
    for i in range(40):
        print(f"Model: {model_name}, Iteration: {i + 1}")
        
        # Generate text and code with the selected model
        if model_name == "qwen2.5-coder":
            response, llm_runtime = generate_text_with_huggingface(prompt, selected_model)
        else:
            response, llm_runtime = generate_text_with_ollama(prompt, selected_model)
        code = extract_code(response)

        # Save the code to a file
        with open(f"data/{test_case_name}/code/{model_name}_{i + 1}.py", "w") as f:
            f.write(code)
        
        # Execute the code and capture the result
        exec_result, code_runtime, error = exec_code(model_name, i + 1)
        
        # Extract individual attributes from exec_result if it is a dictionary
        if isinstance(exec_result, dict):
            for req in requirements:
                requirements[req] = exec_result.get(req)
        else:
            for req in requirements:
                requirements[req] = None
        
        # Append the results to the list for CSV export
        results_list.append({
            "Model": model_name,
            "Iteration": i + 1,
            # "Generated_Code": code,
            "LLM_Response_Time (s)": llm_runtime,
            "Code_Execution_Time (s)": code_runtime,
            # "Execution_Output": exec_result,
            **{req: requirements[req] for req in requirements}, 
            "Error": error
        })

        # Save runtime data to the text file
        with open(f"data/{test_case_name}/output/" + model_name + ".txt", "a") as f:
            f.write(f"Iteration {i + 1}:\n")
            if code_runtime is not None:
                f.write(f"LLM Response Time: {llm_runtime:.4f} sec, Code Execution Time: {code_runtime:.4f} sec\n")
                for req in requirements:
                    f.write(f"{req}: {requirements[req]} ")
                f.write("\n")
            else:
                f.write(f"LLM Response Time: {llm_runtime:.4f} sec, Code Execution failed\n")
                f.write(f"Error: {error}\n")
            f.write("\n")

# Create a DataFrame from the results list and save it to a CSV
results_df = pd.DataFrame(results_list)
results_df.to_csv(f"data/{test_case_name}/code_execution_results.csv", index=False)
print("Results saved to data/code_execution_results.csv")