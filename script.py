import json
import sys
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    print(input_data)
    sys.stdout.flush()
    text_to_evaluate = "Bonjour ma belle"

    output_data = {
        "is_polite":is_text_polite(text_to_evaluate)
    }
    response = json.dumps(output_data)

    return response
