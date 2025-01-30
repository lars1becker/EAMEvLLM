import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Function to generate text using Cerebras
def generate_text_with_huggingface(prompt, model, embed, file, coding_language="python"):
    client = InferenceClient(headers={"x-use-cache": "false"}, api_key=HUGGINGFACE_API_KEY)
    prompt = f"Can you write me {coding_language} code that extracts: " + prompt + " from the file " + file.name + ", which is at the path ./data/uploads/" + file.name + f". Save the result to a variable called result and print it out. Use the most common {coding_language} libraries. Just give the code block as output without any additional text. Make sure the code works correctly and compiles. {"Name the class Code."  if coding_language == "java" else ""}" if embed else prompt

    # New conversation 
    conversation = []
    conversation.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model=model, 
    	messages=conversation, 
    	max_tokens=1000
    )
    conversation.append({"role": "assisstant", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content, conversation