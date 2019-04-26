import json
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    print(input_data)
    text_to_evaluate = input_data[0]['text']

    output_data = {
        "is_polite":is_text_polite(text_to_evaluate)
    }
    response = json.dumps(output_data)

    return response
