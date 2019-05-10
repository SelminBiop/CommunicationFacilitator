import json
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]

    analyzed_text, is_polite = is_text_polite(text_to_evaluate)

    output_data = {
        "is_polite":is_polite,
        "analyzed_text":analyzed_text
    }
    response = json.dumps(output_data, ensure_ascii=False)

    return response
