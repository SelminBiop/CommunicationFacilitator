import json
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json

    output_data = {
        "is_polite":is_text_polite("")
    }
    response = json.dumps(output_data)

    return response
