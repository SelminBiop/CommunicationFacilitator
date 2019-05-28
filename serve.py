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
            db.insert_email_data(email)
        except:
            sys.stdout.write('Error adding email to database')
            sys.stdout.flush()
        finally:
                document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
                annotations = client.analyze_sentiment(document=document, encoding_type=enums.EncodingType.UTF32)

                email.score = annotations.document_sentiment.score
                email.magnitude = annotations.document_sentiment.magnitude
                email.sentences_from_google_nlp(annotations.sentences)

    db.execute_in_session(action = compute_text_score(analyzed_text, sum_score, email.sentences))
       
    return analyzed_text, sum_score >= 0


def compute_text_score(text, score, sentences):
    for sentence in sentences:
        sentence_sentiment = sentence.sentiment
        sentence_text = sentence.text
        sum_score += sentence_sentiment
        text.append((sentence_text, sentence_sentiment))    