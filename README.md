# Code Generation via Large Language Models to Extract Metadata from Files
###### Streamlit GUI and Testing Environment

### gui-streamlit
##### How to set up?
- create and activate Python virtual environment
- pip install -r requirements
- to run GUI: cd gui-streamlit -> streamlit run finished_app.py
- to access ollama models -> install ollama -> install models -> models should appear in the GUI
- to access models via Hugging Face Inference API -> create Account -> create API token -> enter token into newly created file .env (look at example.env)
- Recommended models: Qwen2.5-Coder-32B-Instruct (via Hugging Face API), Qwen2.5-Coder-3B and Deepseek-Coder-V2-16B (via Ollama)
##### How to integrate other API endpoints?
- add the api request as a Python file to functions/api_modules using *model* and *conversation* as parameters and returning *response* 
- add the model and the associated function to the *models* dict at the start of finished_app.py similar to the already implemented Qwen model

### testing_llms
- Testing of large language models
