# Code Generation via Large Language Models to Extract Metadata from Files
###### Streamlit GUI and Testing Environment

### gui-streamlit
##### How to set up?
- create and activate virtual environment
- pip install -r requirements
- set up .env with own api keys look at example.env
- to access ollama models -> install ollama -> install models -> models should appear in the GUI
##### How to integrate other API endpoints?
- add the api request as a Python file to functions/api_modules using *model* and *conversation* as parameters and returning *response* 
- add the model and the associated function to the *models* dict at the start of finished_app.py similar to the already implemented Qwen model

### testing_llms
- Testing of large language models