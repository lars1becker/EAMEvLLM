import streamlit as st
import re
import pandas as pd
import os
import PyPDF2
from code_editor import code_editor
from huggingface_hub import InferenceClient
import requests

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [
        {"role": "system", "content": "You are a helpful coding assisstant."},
    ]

# Function to generate text using Cerebras
def chat_with_huggingface(prompt, model):
    client = InferenceClient(api_key="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")

    # Append the user's message to the conversation history
    st.session_state['conversation_history'].append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=model, 
    	messages=st.session_state['conversation_history'], 
        max_tokens=1000
    )

    # Get the model's response
    assistant_response = completion['choices'][0]['message']['content']
    
    # Append the assistant's response to the conversation history
    st.session_state['conversation_history'].append({"role": "assistant", "content": assistant_response})

    print(st.session_state['conversation_history'])

    return completion.choices[0].message.content

def text_generation_with_huggingface(prompt, model):
    API_URL = "https://api-inference.huggingface.co/models/" + model
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "x-wait-for-model": "true"
    }
    data = {
        "inputs": prompt,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

st.title("Testing Huggingface API")

# User input
user_input = st.text_area("Testing prompt on LLM:")

# Cerebras models
models = ["Qwen/Qwen2.5-Coder-32B-Instruct", "microsoft/Phi-3-mini-4k-instruct", "microsoft/Phi-3.5-mini-instruct", "Qwen/Qwen2.5-72B-Instruct"]

# Create a dropdown to let the user select a model
if models:
    selected_model = st.selectbox("Select a LLama model", models)
else:
    selected_model = None
    st.error("No models available. Please check your Cerebras.")

# Generate button
if st.button("Generate Text"):
    if user_input:
        if selected_model:
            st.write(chat_with_huggingface(user_input, selected_model))
        else:
            st.warning("Please select a model.")
    else:
        st.warning("Please enter a prompt.")