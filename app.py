from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  # Google AI API endpoint
API_KEY = os.getenv("GOOGLE_API_KEY") # Google API key

@app.route('/')
def index():
  return send_from_directory('static', 'index.html')

@app.route('/api/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    payload = {
       "contents": [{
           "parts":[{
               "text": prompt
           }]
       }]
   }
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': API_KEY, # Google API key
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status() # This raises an exception for HTTP errors
        response_data = response.json()

       # Extract the text from the response.
        if 'candidates' in response_data and response_data['candidates']:
           text_response = response_data['candidates'][0]['content']['parts'][0]['text']
        else:
           text_response = "Could not get text from API response"


        return jsonify({'response': text_response}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 500
    except Exception as e:
         return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)