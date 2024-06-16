# The following software is necessary to run this application locally:
- Python 3.7+
- Pip

# To run the application locally, follow these steps:
1. Clone the repository
2. Copy the .env.sample file to a new file called .env
3. Fill in the required environment variables (OPENAI_API_KEY and LANGCHAIN_API_KEY (optional, for tracing only)) in the .env file. 
    - You can get the OPENAI_API_KEY from https://openai.com/index/openai-api/
      (note that you also need to buy OpenAI API credits to use the application)
    - If you want to enable tracing, you also need LANGCHAIN_API_KEY from https://python.langchain.com/v0.1/docs/get_started/quickstart/
4. Install the required dependencies by running `pip install -r requirements.txt`
5. Run the application by running `python app.py`
6. Open your browser and navigate to `http://localhost:5000/`
```
