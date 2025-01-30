import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

def generate_new_code(prompt, model, conversation, coding_language="python"):
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    embedded_prompt = f"Can you rewrite the {coding_language} code. " + prompt

    # Extend the conversation
    conversation.append({"role": "user", "content": embedded_prompt})
    completion = client.chat.completions.create(
        model=model, 
    	messages=conversation, 
    	max_tokens=1000
    )
    conversation.append({"role": "assisstant", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content, conversation