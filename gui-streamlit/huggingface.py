import streamlit as st
import re
import pandas as pd
import os
from code_editor import code_editor
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import subprocess
import time
from code_editor_custom import get_code_editor

# Initialize session state
if "generated_code" not in st.session_state:
    st.session_state["generated_code"] = None
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Function to extract code from a response
def extract_code(response_text):
    # Use regex to extract text within code blocks (```)
    match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip() # Return the content inside the code block
    return response_text.strip()  # If no code block, return the raw response

# Function to generate text using Cerebras
def generate_text_with_huggingface(prompt, model):
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    embedded_prompt = "Can you write me python code that extracts: " + prompt + " from the file " + st. session_state['uploaded_file'].name + ", which is at the path ./data/uploads/" + st.session_state['uploaded_file'].name + ". Save the result to a variable called result and print it out. Use the most common python libraries. Just give the code block as output without any additional text. Make sure the code works correctly and compiles."
    conversation = st.session_state["conversation"]
    conversation.append({"role": "user", "content": embedded_prompt})
    completion = client.chat.completions.create(
        model=model, 
    	messages=conversation, 
    	max_tokens=1000
    )
    conversation.append({"role": "assisstant", "content": completion.choices[0].message.content})
    st.session_state["conversation"] = conversation
    return completion.choices[0].message.content

def generate_new_code(prompt, model):
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    embedded_prompt = "Can you rewrite the python code. " + prompt
    conversation = st.session_state["conversation"]
    conversation.append({"role": "user", "content": embedded_prompt})
    completion = client.chat.completions.create(
        model=model, 
    	messages=conversation, 
    	max_tokens=1000
    )
    conversation.append({"role": "assisstant", "content": completion.choices[0].message.content})
    st.session_state["conversation"] = conversation
    return completion.choices[0].message.content

def exec_code(timeout=10):
    try:
        # Start the subprocess with a timeout
        process = subprocess.Popen(
            ["python", f"./data/code.py"],
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

st.title("Code Generator using Huggingface API")

# File uploader
uploaded_file = st.file_uploader(key="huggingface", label="Choose a file")
if uploaded_file:
    with open("data/uploads/" + uploaded_file.name, "wb") as file:
        file.write(uploaded_file.getbuffer())

# Check if a file is uploaded
if uploaded_file is not None:
    # Save the file content to session state
    st.session_state["uploaded_file"] = uploaded_file

# User input
user_input = st.text_area("Just list the metadata extraction requirements for the provided file:")

# Cerebras models
# !!! Other models may require different function to be called otherwise many errors occur
models = ["Qwen/Qwen2.5-Coder-32B-Instruct"]

# Create a dropdown to let the user select a model
if models:
    selected_model = st.selectbox("Select a model", models)
else:
    selected_model = None
    st.error("No models available. Please check Huggingface.")

# Generate button
if st.button("Generate Code"):
    if user_input:
        if selected_model:
            if uploaded_file:
                with st.spinner('Generating code...'):
                    code = extract_code(generate_text_with_huggingface(user_input,selected_model))
            else:
                st.warning("Please provide a file.")
        else:
            st.warning("Please select a LLama model.")
    else:
        st.warning("Please enter a prompt.")

# Run the generated code with the uploaded file content
if code is not None:
    code = get_code_editor(code=st.session_state['generated_code'])  
    st.session_state['generated_code'] = code['text']
    print(st.session_state['generated_code'])
    
    col1, col2 = st.columns(spec=[0.5,0.5], gap='small')

    with col1:
        # A button to execute the code
        if st.button("Execute Code on provided File", use_container_width=True, disabled=False):
            try:
                # Save the code to a file
                with open(f"data/code.py", "w") as f:
                    f.write(code['text'])

                # Execute the dynamically generated code (user input code) in this context
                output = exec_code(10)

                # Display success message
                st.success("Code executed successfully!")

                # Capture and display the output or result variables from local_scope
                st.write(output)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    with col2:
        if(st.button(label="Generate new Code snippet", disabled=False, use_container_width=True)):
            st.session_state['generated_code'] = extract_code(generate_new_code("", selected_model))