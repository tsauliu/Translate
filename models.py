from openai import OpenAI
from env import api_key
import os
prompt_content = open('prompt.md', 'r', encoding='utf-8').read()

def translate_text_deepseek(text):
    client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=api_key
    )

    completion = client.chat.completions.create(
        model="bot-20250320164908-pfqfh",  
        messages=[
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": text},
        ],
    )
    result = completion.choices[0].message.content
    cleaned_result = '\n'.join([line for line in result.splitlines() if line.strip()])
    return cleaned_result

from google import genai
from google.genai import types
from env import gemini_key

def translate_text_gemini(text):
    client = genai.Client(api_key=gemini_key)
    modelname="gemini-2.5-flash-preview-05-20" #gemini-2.5-pro-preview-06-05，gemini-2.5-flash-preview-05-20
    # print(f'{modelname} is used')
    response = client.models.generate_content(
        model=modelname,
        config=types.GenerateContentConfig(
        temperature=1
        ) , 
        contents=prompt_content+'\n -- \n'+text 
    )
    return response.text