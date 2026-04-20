import uuid
import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

api_endpoint = os.getenv('api_endpoint')
api_key = os.getenv('api_key')
api_region = os.getenv('api_region')

@app.get('/api/status')
def health():
    return {'status': 'Healthy'}

@app.post('/api/translate')
def translate():
    data = request.get_json()

    if 'text' not in data or data['text'] == '':
        response = {
            'status': 'error',
            'error': 'Text was not provided.'
        }
        return jsonify(response)
    
    if 'lang' not in data:
        response = {
            'status': 'error',
            'error': 'Target language was not specified.'
        }
        return jsonify(response)

    url = api_endpoint + '/translate?api-version=3.0&to=' + data['lang']

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': api_region,
        'Content-Type': 'application/json; charset=UTF-8',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    request_body = [{
        'text': data['text']
    }]

    try:
        r = requests.post(url, headers=headers, json=request_body)
    except Exception as e:
        response = {
            'status': 'error',
            'error': e
        }
        return jsonify(response)

    if r.status_code != 200:
        response = {
            'status': 'error',
            'error': r.text
        }

    response_json = r.json()
    print(response_json)

    response = {
        'status': 'success',
        'translation': response_json[0]['translations'][0]['text']
    }
    print(response)

    return jsonify(response)

if __name__ == '__main__':
    # Dev-only fallback
    app.run(host='0.0.0.0', port=8000, debug=True)