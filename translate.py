#%%
import os
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from env import api_key

app = Flask(__name__)

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    # 从环境变量中获取您的 API Key
    api_key=api_key
)

# Read the translation prompt from the markdown file
prompt_content = open('prompt.md', 'r', encoding='utf-8').read() if os.path.exists('prompt.md') else "Translate the following text to English. If it's already in English, improve it."

def translate_text(text):
    completion = client.chat.completions.create(
        model="bot-20250320164908-pfqfh",  # bot-20250320164908-pfqfh 为您当前的智能体的ID，注意此处与Chat API存在差异。差异对比详见 SDK使用指南
        messages=[
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.json['text']
        if not text:
            return jsonify({'error': 'Please enter some text to translate'}), 400
        
        translated_text = translate_text(text)
        return jsonify({'translation': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create static folder for favicon
if not os.path.exists('static'):
    os.makedirs('static')

# Create a simple favicon if it doesn't exist
if not os.path.exists('static/favicon.ico'):
    # Create an empty favicon file
    open('static/favicon.ico', 'w').close()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)