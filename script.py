import json
import datetime
from email import Email
from flask import Flask, request
from serve import is_text_polite

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]
    sender = input_data["sender"]
    receiver = input_data["receiver"]
    received_year = int(input_data["received_year"])
    received_month = int(input_data["received_month"])
    received_date = int(input_data["received_date"])
    subject = input_data["subject"]

    email = Email()

    email.receiver = receiver
    email.sender = sender
    email.received = datetime.date(received_year, received_month, received_date)
    email.subject = subject

    analyzed_text, is_polite = is_text_polite(text_to_evaluate, email)

    output_data = {
        "is_polite":is_polite,
        "analyzed_text":analyzed_text
    }
    response = json.dumps(output_data, ensure_ascii=False)

    return response
