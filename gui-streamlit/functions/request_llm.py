
def request_llm(prompt, model, function, embed, conversation, file):
    if embed:
        prompt = f"You are an expert at writing Python code. Can you write me Python code that extracts: {prompt} from the {file.type} file, which path is given as the first argv. Save the result to a variable called result and print it out. Use the most common Python libraries. Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text. Make sure the code works correctly and compiles."
    else:
        prompt = f'Can you write me Python code. {prompt} The filepath is given as the first argv.  Just give the code block like this: ```python ... ``` and the libraries used like this: ```requirements ... ``` as output without any additional text. Make sure the code works correctly and compiles.'

    conversation.append({"role": "user", "content": prompt})

    # Call the API request function based on the model
    response = function(model, conversation)
    
    conversation.append({"role": "assistant", "content": response})

    return response, conversation