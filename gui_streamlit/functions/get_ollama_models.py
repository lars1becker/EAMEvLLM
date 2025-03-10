import ollama

from functions.llm_api_modules.ollama_api import ollama_api_request

# Function to fetch Ollama models available
def get_ollama_models():
    try:
        models = ollama.list()
        model_names = {}
        for model in models['models']:
            model_names[model['model']] = ollama_api_request
 
        if len(model_names) != 0:
            return model_names
        else:
            print("Error fetching models:", models.stderr)
            return {}
    except Exception as e:
        print("Error:", str(e))
        return {}