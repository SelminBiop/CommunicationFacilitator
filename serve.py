from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from modelDatabase import ModelDatabase
from emailSentiment import EmailSentiment
import sys

client = language.LanguageServiceClient()
db = ModelDatabase()
db.connect()

def is_text_polite(text, email):    
    sum_score = 0
    analyzed_text = []
    try:
        email = db.retrieve_email_data(email)
    except:        
        sys.stdout.write('Email not in database')
        sys.stdout.flush()
        try:
            document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
            annotations = client.analyze_sentiment(document=document, encoding_type=enums.EncodingType.UTF32)

            email.score = annotations.document_sentiment.score
            email.magnitude = annotations.document_sentiment.magnitude
            email.sentences_from_google_nlp(annotations.sentences)
            email = db.insert_email_data(email)
        except:
            sys.stdout.write('Error adding email to database')
            sys.stdout.flush()                

    for sentence in email.sentences:
        sum_score += sentence.sentiment
        analyzed_text.append((sentence.text, sentence.sentiment, sentence.id))
       
    return analyzed_text, sum_score >= 0


def update_sentence(sentence_id, sentiment):
    try:
        db.update_sentence_sentiment(sentence_id, sentiment)
    except:
        sys.stdout.write('Error updating sentence sentiment')
        sys.stdout.flush()
        return False
    return True