import re
# Function to extract code from a response
def extract_code(response_text):
    # Use regex to extract text within code blocks (```)
    match = re.search(rf"```python\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip() # Return the content inside the code block
    return None