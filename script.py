import json
import datetime
from emailSentiment import EmailSentiment
from flask import Flask, request
from flask import Response
from serve import is_text_polite
from serve import update_sentence

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]
    sender = input_data["sender"]
    subject = input_data["subject"]
    received_year = int(input_data["received_year"])
    received_month = int(input_data["received_month"])
    received_date = int(input_data["received_date"])

    email = EmailSentiment()

    email.sender = sender
    email.subject = subject
    email.received = datetime.date(received_year, received_month, received_date)

    analyzed_text, is_polite = is_text_polite(text_to_evaluate, email)

    output_data = {
        "is_polite":is_polite,
        "analyzed_text":analyzed_text
    }
    js = json.dumps(output_data, ensure_ascii=False)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

@app.route('/update', methods=['PUT'])
def update():
    input_data = request.json
    sentence_id = input_data["sentence_id"]
    sentiment = input_data["sentiment"]

    status = 200 if update_sentence(sentence_id, sentiment) else 400

    return Response(status=status)