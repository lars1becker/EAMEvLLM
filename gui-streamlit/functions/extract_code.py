import re
# Function to extract code from a response
def extract_code(response_text, coding_language="python"):
    # Use regex to extract text within code blocks (```)
    match = re.search(rf"```{coding_language}\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip() # Return the content inside the code block
    return None