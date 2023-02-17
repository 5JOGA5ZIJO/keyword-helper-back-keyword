import openai
import argparse
from dotenv import load_dotenv
import os

# 환경변수 가져오기
load_dotenv()
_OPENAI_API = os.environ.get("OPENAI_API")

def chatGPT(prompt, API_KEY=_OPENAI_API):    
    openai.api_key = API_KEY

    # Call the chat GPT API
    completion = openai.Completion.create(
			  engine = 'text-davinci-003'     # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
			, prompt =  prompt
			, temperature = 0.5 
			, max_tokens = 1024
			, top_p = 1
			, frequency_penalty = 0
			, presence_penalty = 0
            , stop='')

    return completion['choices'][0]['text']
    # OpenAI API endpoint
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"

    # Your API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # The prompt to generate text from
    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7,
        "n": 1,
        "stop": "\n"
    }

    # Send the request to the API
    response = requests.post(url, headers=headers, json=data)

    # Get the response from the API
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        raise Exception(f"Failed to generate text. Response: {response.content}")