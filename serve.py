from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from database import Database
import psycopg2
import sys

client = language.LanguageServiceClient()

def is_text_polite(text, email):    

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document, encoding_type=enums.EncodingType.UTF32)

    email.score = annotations.document_sentiment.score
    email.magnitude = annotations.document_sentiment.magnitude
    email.sentences = annotations.sentences

    sum_score = 0

    analyzed_text = []

    try:
        conn = Database()
        conn.connect()
        conn.insert_email_data(email)
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stdout.write(str(error))
    finally:
        conn.close()

    for sentence in annotations.sentences:
        sentence_sentiment = sentence.sentiment.score
        sentence_text = sentence.text.content
        sum_score += sentence_sentiment
        analyzed_text.append((sentence_text, sentence_sentiment))    

    return analyzed_text, sum_score >= 0