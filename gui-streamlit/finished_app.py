import os
import streamlit as st
import requests
import time

from functions.create_zip import create_zip
from functions.exec_code_venv import exec_code_venv
from functions.extract_code import extract_code
from functions.request_llm import request_llm
from functions.switch_tab import switch_tab
from functions.fetch_file_using_url import fetch_file_using_url
from functions.get_ollama_models import get_ollama_models
from functions.test_zip import test_zip

# Constants
GENERATED_CODE_PATH = "temp/zip/Generated_Code.py"
UPLOAD_PATH = "data/uploads/"

# Set the page config to be full width
st.set_page_config(layout="wide")

# Initialise session states
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "code_execution_response" not in st.session_state:
    st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }
if "llm_response_time" not in st.session_state:
    st.session_state.llm_response_time = None
if "zip_bytes" not in st.session_state:
    st.session_state.zip_bytes = None

# Set the title of the app
st.title("DBpedia Databus Mods Code Generator")

# Get the available models and append API models
models = get_ollama_models()
models.append("Qwen/Qwen2.5-Coder-32B-Instruct")

# Create a dropdown to let the user select a model
if models:
    selected_model = st.selectbox("Select a model", models)
else:
    selected_model = None
    st.error("No models available.")

if st.session_state.llm_response_time:
    st.info(f"LLM response time: {st.session_state.llm_response_time:.2f} seconds")

# Layout with tabs
tabs = st.tabs(["📄 Upload File \\ ⚙️ Generate Code", "🔧 Refine Code"])

# ==============================
# Upload File and Generate Code Tab
# ==============================
with tabs[0]:
    # ==============================
    # Upload File Component
    # ==============================
    uploaded_file, error = None, None

    upload_variant = st.radio("Select the upload variant", ["device", "url"], index=0, horizontal=True)

    # Upload the file using the chosen variant
    if(upload_variant == "device"):
        # Streamlit file upload
        uploaded_file = st.file_uploader("Upload a file from your device:")
    elif(upload_variant == "url"):
        file_url = st.text_input("Provide a file URL (max 200MB):")
        max_size = 200 * 1024 * 1024  # 200MB
        error = None
        # Handle URL input
        if st.button("Fetch File from URL"):
            if file_url != "":
                with st.spinner("Fetching the file..."):
                    try:
                        uploaded_file, error = fetch_file_using_url(file_url, max_size)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Failed to fetch the file: {e}")
            else: 
                st.warning("Please provide a file URL.")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        # st.toast("File uploaded successfully!", icon="✅")
    elif error:
        st.error(error)
    if st.session_state.uploaded_file:
        st.info(f"File uploaded. Filename: {st.session_state.uploaded_file.name}, Filesize: {len(st.session_state.uploaded_file.getbuffer()) / 1024:.3f} KB")
        with open(UPLOAD_PATH + st.session_state.uploaded_file.name, "wb") as file:
            file.write(st.session_state.uploaded_file.getbuffer())
        # st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }

    # ==============================
    # Prompt component
    # ==============================
            
    # Radio button to select the prompt setting
    prompt_setting = st.radio(
        "Toggle", 
        options=["Template", "Custom"],
        index=1,
        horizontal=True,
        captions=("Use template prompt to just enter metadata extraction requirements.", "Create own prompt (with template for processing)."),
        label_visibility="collapsed",
        key='first'
    )

    user_input = None

    prompt = ""
    # Disable the "Template" radio option in a conditional way
    if st.session_state.uploaded_file is None:
        st.warning("Please provide a file to enter a prompt.")
    elif prompt_setting == "Template":
        user_input = st.text_area("Just enter the metadata extraction requirements:", height=100)
        prompt = f'You are an expert at writing Python code. Can you write me Python code that extracts: <span style="color:red">{user_input if user_input != "" else "{ requirements }"}</span> from the file, which path is given as the first argv. Save the result to a variable called result and print it out. Use the most common Python libraries. Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text. Make sure the code works correctly and compiles.'
    else:
        user_input = st.text_area("Enter a custom prompt to generate code snippet:", height=100)
        prompt = f'Can you write me Python code. <span style="color:red">{user_input if user_input != "" else "{ user prompt }"}</span>. The filepath is given as the first argv. Save the result to a variable called result and print it out. Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text.'

    st.markdown(f'<p style="background-color:#1b2b42;color:white;font-size:16px;border-radius:8px;padding:12px;"> <span style="color:gray"> Prompt: </span> <br>{prompt}</p>', unsafe_allow_html=True)

    # Generate button
    if st.button("Generate Code", use_container_width=True):
        if user_input:
            if selected_model:
                with st.spinner('Generating code...'):
                    start_time = time.time()
                    response, st.session_state.conversation = request_llm(user_input, selected_model, prompt_setting == "Template", [])
                    st.session_state.llm_response_time = time.time() - start_time
                    st.session_state.generated_code = extract_code(response)
                    # Save the code to a file
                    with open(GENERATED_CODE_PATH, "w") as f:
                        f.write(st.session_state.generated_code)
                    if st.session_state.generated_code:
                        st.toast("Code generated successfully!")
                        st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }
                        switch_tab("🔧 Refine Code")
                    else:
                        st.toast("Failed to generate code.", icon="🚨")
            else:
                st.warning("Please select a model.")
        else:
            st.warning("Please enter a prompt.")

# ==============================
# Refine and Execute Code Tab
# ==============================
with tabs[1]:
    if st.session_state.generated_code is not None and st.session_state.generated_code != "":
        # ==============================
        # Code editor component
        # ==============================
        col1, col2 = st.columns(spec=[0.5,0.5], gap='small')
        with col1:
            st.code(st.session_state.generated_code, line_numbers=True, language=f"python", wrap_lines=True)
            if(st.button(label="Automatically Generate New Code Snippet", disabled=False, use_container_width=True)):
                start_time = time.time()
                response, st.session_state.conversation = request_llm(f"Can you rewrite the Python code.", selected_model, False, st.session_state.conversation)
                st.session_state.llm_response_time = time.time() - start_time
                st.session_state.generated_code = extract_code(response)
                # Save the code to a file
                with open(GENERATED_CODE_PATH, "w") as f:
                    f.write(st.session_state.generated_code)
                st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }
                st.rerun()
        with col2:
            code = st.text_area(label="Edit Code Text Area",value=st.session_state.generated_code, height=max(200,st.session_state.generated_code.count("\n") * 28), label_visibility="collapsed")
            if st.button("Save Edited Code", use_container_width=True):
                # Save the edited code to the session state
                st.session_state.generated_code = code
                # Add the code changes to the conversation
                st.session_state.conversation.append({"role": "user", "content": f"I manually changed the code to this: {code}"})
                # Save the code to a file
                with open(GENERATED_CODE_PATH, "w") as f:
                    f.write(st.session_state.generated_code)
                st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }
                st.rerun()

        # ==============================
        # New Code Generation using Prompt Component
        # ==============================
        user_prompt = st.text_area("Enter a prompt to generate new code snippet:")
        if st.button("Generate New Code Snippet using Prompt", use_container_width=True):
            if user_prompt:
                start_time = time.time()
                response, st.session_state.conversation = request_llm(user_prompt, selected_model, False, st.session_state.conversation)
                st.session_state.llm_response_time = time.time() - start_time
                st.session_state.generated_code = extract_code(response)
                # Save the code to a file
                with open(GENERATED_CODE_PATH, "w") as f:
                    f.write(st.session_state.generated_code)
                st.session_state.code_execution_response = { "output": "", "code_runtime": "", "code_space": "" }
                st.rerun()
            else:
                st.warning("Please enter a prompt.")

        # ==============================
        # Code Execution Component
        # ==============================
        if st.button("Execute Code on provided File", use_container_width=True, disabled=False):
            try:
                # Execute the dynamically generated code (user input code) in this context
                output, code_runtime, code_space = exec_code_venv(GENERATED_CODE_PATH, UPLOAD_PATH + st.session_state.uploaded_file.name, 10)
                st.session_state.code_execution_response = {"output": output, "code_runtime": code_runtime, "code_space": code_space}
            except Exception as e:
                st.error(f"An error occurred: {e}")
        if st.session_state.code_execution_response["output"].startswith("Standard Error"):
            st.error("Code execution failed!")
            st.write(st.session_state.code_execution_response["output"])
            if st.button("Generate new Code Snippet using the Error", use_container_width=True):
                    start_time = time.time()
                    response, st.session_state.conversation = request_llm(f"Can you rewrite the code. Using the error: {st.session_state.code_execution_response["output"]}", selected_model, False, st.session_state.conversation)
                    st.session_state.llm_response_time = time.time() - start_time
                    st.session_state.generated_code = extract_code(response)
                    # Save the code to a file
                    with open(GENERATED_CODE_PATH, "w") as f:
                        f.write(st.session_state.generated_code)
                    st.rerun()
        elif st.session_state.code_execution_response["output"] != "":
            # Display success message
            st.success("Code executed successfully!")
            # Capture and display the output or result variables from local_scope
            st.write("Output: " + st.session_state.code_execution_response["output"])
            st.info("Code runtime: " + st.session_state.code_execution_response["code_runtime"] + " seconds, Memory usage: " + st.session_state.code_execution_response["code_space"] + " KB")
    
        # ==============================
        # Create ZIP file and download Component
        # ==============================
        col1, col2 = st.columns(spec=[0.5, 0.5], gap="small")

        if st.session_state.code_execution_response["output"] != "" and not st.session_state.code_execution_response["output"].startswith("Standard Error"):
            with col1:
                if st.button("Generate Zip", use_container_width=True):
                    zip_path = create_zip(GENERATED_CODE_PATH, [UPLOAD_PATH + st.session_state.uploaded_file.name] if st.session_state.uploaded_file else [])
                    # Read ZIP file as bytes
                    if zip_path.startswith("Failed to generate"):
                        st.toast(zip_path, icon="🚨")
                    else:
                        # Test the ZIP file
                        if test_zip(os.path.dirname(GENERATED_CODE_PATH), st.session_state.uploaded_file.name):
                            with open(zip_path, "rb") as f:
                                st.session_state.zip_bytes = f.read()
                            st.toast("Zip file generated successfully.", icon="🎉")
                        else:
                            st.toast("The zip file could not be generated.", icon="🚨")

            with col2:
                st.download_button(
                    label="Download Zip",
                    data=st.session_state.zip_bytes if st.session_state.zip_bytes is not None else b"",
                    file_name="app.zip",
                    mime="application/zip",
                    use_container_width=True,
                    disabled=st.session_state.zip_bytes is None  # Disable if no ZIP file is generated
                )
        else:
            st.warning("Code execution is required to generate the ZIP file.")
            st.session_state.zip_bytes = None

    else:
        st.info("No code available to refine. Please generate code first.", icon="ℹ️")