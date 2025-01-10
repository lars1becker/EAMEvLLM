import streamlit as st
import ollama
import re
import pandas as pd
import os
from code_editor import code_editor
    
# Initialize session state
if "generated_code" not in st.session_state:
    st.session_state["generated_code"] = None
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None


# Function to extract code from a response
def extract_code(response_text):
    # Use regex to extract text within code blocks (```)
    match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip() # Return the content inside the code block
    return response_text.strip()  # If no code block, return the raw response

# Function to generate text using Ollama
def generate_text_with_ollama(prompt, model):
    embedded_prompt = "Can you write me python code that extracts: " + prompt + " from the file " + st. session_state['uploaded_file'].name + ", which is at the path ./" + st.session_state['uploaded_file'].name + ". Save the result to a variable called result and use the mostly used common libraries."

    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': embedded_prompt,
    },
    ])
    return response['message']['content']

# Function to fetch Ollama models available
def get_ollama_models():
    try:
        result = ollama.list()
        if len(result) != 0:
            model_names = [model['name'] for model in result['models']]
            return model_names
        else:
            print("Error fetching models:", result.stderr)
            return []
    except Exception as e:
        print("Error:", str(e))
        return []
    
st.title("Code Generator using Ollama")

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    with open("data/uploads/" + uploaded_file.name, "wb") as file:
        file.write(uploaded_file.getbuffer())

# Check if a file is uploaded
if uploaded_file is not None:
    # Save the file content to session state
    st.session_state["uploaded_file"] = uploaded_file

# User input
user_input = st.text_area("Just list the metadata extraction requirements for the provided file:")

# Fetch models
models = get_ollama_models()

# Create a dropdown to let the user select a model
if models:
    selected_model = st.selectbox("Select an Ollama model", models)
else:
    selected_model = None
    st.error("No models available. Please check your Ollama installation.")

# Generate button
if st.button("Generate Code"):
    if user_input:
        if selected_model:
            if uploaded_file:
                with st.spinner('Generating code...'):
                    st.session_state['generated_code'] = extract_code(generate_text_with_ollama(user_input,selected_model))
            else:
                st.warning("Please provide a file.")
        else:
            st.warning("Please select an Ollama model.")
    else:
        st.warning("Please enter a prompt.")

# Run the generated code with the uploaded file content
if st.session_state['generated_code'] is not None:
    # Add a button with text: 'Copy'
    # create copy button with 'infoMessage' command
    custom_btns = [{
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll", 
                     ["infoMessage", 
                      {
                       "text":"Copied to clipboard!",
                       "timeout": 2500, 
                       "classToggle": "show"
                      }
                     ]
                    ],
        "style": {"right": "0.4rem"}
    }]
    css_string = '''
    background-color: #bee1e5;

    body > #root .ace-streamlit-dark~& {
       background-color: #262830;
    }

    .ace-streamlit-dark~& span {
       color: #fff;
       opacity: 0.6;
    }

    span {
       color: #000;
       opacity: 0.5;
    }

    .code_editor-info.message {
       width: inherit;
       margin-right: 75px;
       order: 2;
       text-align: center;
       opacity: 0;
       transition: opacity 0.7s ease-out;
    }

    .code_editor-info.message.show {
       opacity: 0.6;
    }

    .ace-streamlit-dark~& .code_editor-info.message.show {
       opacity: 0.5;
    }
    '''
    # create info bar dictionary
    info_bar = {
      "name": "language info",
      "css": css_string,
      "style": {
                "order": "1",
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "center",
                "width": "100%",
                "height": "2.5rem",
                "padding": "0rem 0.75rem",
                "borderRadius": "8px 8px 0px 0px",
                "zIndex": "9993"
               },
      "info": [{
                "name": "python",
                "style": {"width": "100px"}
               }]
    }
    code = code_editor(code=st.session_state['generated_code'], buttons=custom_btns, info=info_bar, options={'wrap':True, 'showLineNumbers':True}) 
    
    col1, col2 = st.columns(spec=[0.5,0.5], gap='small')

    with col1:
        # A button to execute the code
        if st.button("Execute Code on provided File", use_container_width=True, disabled=False):
            try:
                # Prepare a dictionary for local and global variables during execution
                global_scope = {
                    'os': os,  # Make 'os' available globally
                    'pd': pd,  # Make 'pandas' available globally
                    're': re,
                }
                local_scope = {}

                # Execute the dynamically generated code (user input code) in this context
                exec(code['text'], global_scope, local_scope)

                # Display success message
                st.success("Code executed successfully!")

                # Capture and display the output or result variables from local_scope
                output_found = False
                for key, value in local_scope.items():
                    if not key.startswith("__") and key == "result":  # Avoid private/internal attributes
                        output_found = True
                        st.write(f"**{key}**: {value}")

                # If no output variables were created, display a generic message
                if not output_found:
                    st.write("No output variables were generated.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    with col2:
        if(st.button(label="Deploy Mod to DBpedia Datbus", disabled=True, use_container_width=True)):
            pass