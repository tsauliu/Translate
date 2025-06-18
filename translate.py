#%%
import os
from flask import Flask, render_template, request, jsonify
from models import translate_text_gemini, shorten_text_gemini

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.json['text']
        if not text:
            return jsonify({'error': 'Please enter some text to translate'}), 400
        
        translated_text = translate_text_gemini(text)
        return jsonify({'translation': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        text = request.json['text']
        if not text:
            return jsonify({'error': 'Please enter some text to shorten'}), 400
        
        shortened_text = shorten_text_gemini(text)
        return jsonify({'shortened_text': shortened_text})
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
    app.run(debug=True,host='0.0.0.0',port=9000)