import json
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]

    output_data = {
        "is_polite":is_text_polite(text_to_evaluate)
    }
    response = json.dumps(output_data)

    return response
