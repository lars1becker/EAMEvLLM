
def request_llm(prompt, model, function, conversation):
    
    conversation.append({"role": "user", "content": prompt})

    # Call the API request function based on the model
    response = function(model, conversation)
    
    conversation.append({"role": "assistant", "content": response})

    return response, conversation