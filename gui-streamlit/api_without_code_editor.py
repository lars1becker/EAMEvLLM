import streamlit as st

from functions.create_zip import create_zip
from functions.exec_code import exec_code
from functions.extract_code import extract_code
from functions.generate_new_code import generate_new_code
from functions.generate_text_huggingface import generate_text_with_huggingface
from functions.switch_tab import switch_tab
from functions.create_dockerfile import create_dockerfile
from functions.create_requirements import create_requirements
from functions.create_readme import create_readme
from functions.create_docker_compose import create_docker_compose

import requests
from io import BytesIO 

coding_language = "python"

# Initialize session state
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.set_page_config(layout="wide")

st.title("Code Generator using Huggingface API")

# Layout with tabs
tabs = st.tabs(["📄 Upload File \\ ⚙️ Generate Code", "🔧 Refine Code"])

with tabs[0]:
    uploaded_file = None

    upload_variant = st.radio("Select the upload variant", ["device", "url"], index=0, horizontal=True)
    if(upload_variant == "device"):
        # Streamlit file upload
        uploaded_file = st.file_uploader("Upload a file from your device:")

        # Handle uploaded file
        if uploaded_file is not None:
            st.write(f"File uploaded: {uploaded_file.name}")
            st.session_state.uploaded_file = uploaded_file
    else:
        # URL input for HTTP file upload
        file_url = st.text_input("Provide a file URL (max 200MB):")

        file = None  # To hold the file object

        max_size = 200 * 1024 * 1024  # 200MB

        # Handle URL input
        if st.button("Fetch File from URL") and file_url:
            with st.spinner("Fetching the file..."):
                try:
                    # Fetch file from URL
                    response = requests.get(file_url, stream=True)
                    response.raise_for_status()  # Raise an error for HTTP issues
                    # Check if the file size exceeds the maximum allowed size
                    if int(response.headers.get("Content-Length", 0)) > max_size:
                        st.error(f"File exceeds the maximum allowed size of {max_size / 1024 / 1024}MB.")
                    else:
                        file = BytesIO(response.content)
                        file.name = file_url.split("/")[-1]  # Set a name for the file
                        st.write(f"File fetched from URL")
                        st.write(f"filename: {file.name}")
                        st.write(f"file size: {len(file.getbuffer())} bytes")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to fetch the file: {e}")

        # Process the file
        if file:
            # Example: Displaying the content of the file
            st.session_state.uploaded_file = file
            st.write(f"Processing file: {file.name}")

    if st.session_state.uploaded_file:
        with open("data/uploads/" + st.session_state.uploaded_file.name, "wb") as file:
            file.write(st.session_state.uploaded_file.getbuffer())
    
    # Create radio button for prompt setting
    prompt_setting = st.radio(
        "Toggle", 
        options=["Template", "Custom"],
        index=1,
        horizontal=True,
        captions=("Use template prompt to just enter metadata extraction requirements.", "Create completely own prompt."),
        label_visibility="collapsed",
        key='first'
    )

    user_input = None

    # Disable the "Template" radio option in a conditional way
    if prompt_setting == "Template" and st.session_state.uploaded_file is None:
        st.warning("The Template option is currently disabled. Please provide a file to enable it.")
    else:
        user_input = st.text_area("Just enter the metadata extraction requirements:" if prompt_setting == "Template" else "Enter a custom prompt to generate code snippet:", height=150)

    coding_language = st.radio("Select the coding language", ["python", "java"], index=0, horizontal=True)

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
    if st.button("Generate Code", use_container_width=True):
        if user_input:
            if selected_model:
                with st.spinner('Generating code...'):
                    response, st.session_state.conversation = generate_text_with_huggingface(user_input, selected_model, prompt_setting == "Template", file=st.session_state.uploaded_file, coding_language=coding_language)
                    st.session_state.generated_code = extract_code(response, coding_language)
                    # Save the code to a file
                    with open(f"data/code.py" if coding_language == "python" else f"data/Code.java", "w") as f:
                        f.write(st.session_state.generated_code)
                    if st.session_state.generated_code:
                        st.toast("Code generated successfully!")
                        switch_tab("🔧 Refine Code")
                    else:
                        st.toast("Failed to generate code.", icon="🚨")
            else:
                st.warning("Please select a LLama model.")
        else:
            st.warning("Please enter a prompt.")

with tabs[1]:
    # Run the generated code with the uploaded file content
    if st.session_state.generated_code is not None:
        col1, col2 = st.columns(spec=[0.5,0.5], gap='small')
        with col1:
            st.code(st.session_state.generated_code, line_numbers=True, language=f"{coding_language}", wrap_lines=True)
            if(st.button(label="Automatically Generate New Code Snippet", disabled=False, use_container_width=True)):
                response, st.session_state.conversation = generate_new_code("", selected_model, conversation=st.session_state.conversation, coding_language=coding_language)
                st.session_state.generated_code = extract_code(response, coding_language)
                # Save the code to a file
                with open(f"data/code.py" if coding_language == "python" else f"data/Code.java", "w") as f:
                    f.write(st.session_state.generated_code)
                st.rerun()
        with col2:
            code = st.text_area(label="Edit Code Text Area",value=st.session_state.generated_code, height=max(200,st.session_state.generated_code.count("\n") * 28), label_visibility="collapsed")
            if st.button("Save Edited Code", use_container_width=True):
                # Save the edited code to the session state
                st.session_state.generated_code = code
                # Add the code changes to the conversation
                st.session_state.conversation.append({"role": "user", "content": f"I manually changed the code to this: {code}"})
                # Save the code to a file
                with open(f"data/code.py" if coding_language == "python" else f"data/Code.java", "w") as f:
                    f.write(st.session_state.generated_code)
                st.rerun()

        user_prompt = st.text_area("Enter a prompt to generate new code snippet:")
        if st.button("Generate New Code Snippet using Prompt", use_container_width=True):
            if user_prompt:
                response, st.session_state.conversation = generate_new_code(user_prompt, selected_model, conversation=st.session_state.conversation, coding_language=coding_language)
                st.session_state.generated_code = extract_code(response, coding_language)
                # Save the code to a file
                with open(f"data/code.py" if coding_language == "python" else f"data/Code.java", "w") as f:
                    f.write(st.session_state.generated_code)
                st.rerun()
            else:
                st.warning("Please enter a prompt.")

        # A button to execute the code
        if st.button("Execute Code on provided File", use_container_width=True, disabled=False):
            try:
                # Execute the dynamically generated code (user input code) in this context
                output = exec_code(10, coding_language)

                if output.startswith("Standard Error"):
                    st.error("Code execution failed!")
                    st.write(output)
                    if st.button("Generate new Code Snippet using the Error", use_container_width=True):
                        response, st.session_state.conversation = generate_new_code(output, selected_model, conversation=st.session_state.conversation, coding_language=coding_language)
                        st.session_state.generated_code = extract_code(response)
                else:
                    # Display success message
                    st.success("Code executed successfully!")
                    # Capture and display the output or result variables from local_scope
                    st.write(output)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        if st.button("Download Zip packed code", use_container_width=True):
            requirements_link = create_requirements(coding_language, st.session_state.generated_code)
            dockerfile_link = create_dockerfile(coding_language)
            readme_link = create_readme()
            docker_compose_link = create_docker_compose()
            create_zip(["data/code.py" if coding_language == "python" else "data/Code.java", dockerfile_link, requirements_link, readme_link, docker_compose_link], ["data/uploads/" + st.session_state.uploaded_file.name])
    else:
        st.info("No code available to refine. Please generate code first.", icon="ℹ️")