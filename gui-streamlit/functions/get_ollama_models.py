import ollama
# Function to fetch Ollama models available
def get_ollama_models():
    try:
        models = ollama.list()
        model_names = [model['model'] for model in models['models']]
 
        if len(model_names) != 0:
            return model_names
        else:
            print("Error fetching models:", models.stderr)
            return []
    except Exception as e:
        print("Error:", str(e))
        return []