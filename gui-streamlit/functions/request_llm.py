
# Import different API modules
from functions.llm_api_modules.huggingface_api import huggingface_api_request
from functions.llm_api_modules.ollama_api import ollama_api_request

def request_llm(prompt, model, embed, conversation):
    if embed:
        prompt = f"You are an expert at writing Python code. Can you write me Python code that extracts: {prompt} from the file, which path is given as the first argv. Save the result to a variable called result and print it out. Use the most common Python libraries. Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text. Make sure the code works correctly and compiles."
    else:
        prompt = f'Can you write me Python code. {prompt} The filepath is given as the first argv.  Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text. Make sure the code works correctly and compiles.'

    conversation.append({"role": "user", "content": prompt})

    # Call the API request function based on the model
    if model == "Qwen/Qwen2.5-Coder-32B-Instruct":
        response = huggingface_api_request(model=model, conversation=conversation)
    else:
        response = ollama_api_request(model=model, conversation=conversation)
    
    conversation.append({"role": "assistant", "content": response})

    return response, conversation