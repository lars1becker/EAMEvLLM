import ollama

# Use the ollama API to generate a response
def ollama_api_request(model, conversation):
    response = ollama.chat(model=model, messages=conversation)
    return response['message']['content'], conversation