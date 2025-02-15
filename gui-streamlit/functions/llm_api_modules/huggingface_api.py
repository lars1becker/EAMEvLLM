import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Access the Hugging Face Inference API
def huggingface_api_request(model, conversation):
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)

    completion = client.chat.completions.create(
        model=model, 
        messages=conversation, 
        max_tokens=1000
    )
    conversation.append({"role": "assistant", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content, conversation