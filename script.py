import json
import nlputils
from flask import Flask, request
from serve import is_text_polite

fr_dict_path = "data/fr_full.txt"

app = Flask(__name__)
app.config['DEBUG'] = True

utils = NLPutils(fr_dict_path)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]

    corrected_text, is_polite = is_text_polite(text_to_evaluate, utils)

    output_data = {
        "is_polite":is_polite,
        "corrected_text":corrected_text
    }
    response = json.dumps(output_data, ensure_ascii=False)

    return response
