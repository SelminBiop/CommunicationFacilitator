from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import psycopg2
import sys
import os

client = language.LanguageServiceClient()
db_url = os.environ['DATABASE_URL']

def is_text_polite(text):    

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document, encoding_type=enums.EncodingType.UTF32)

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    sum_score = 0

    conn = psycopg2.connect(host=db_url)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE sentences (
            sentence_id SERIAL PRIMARY KEY,
            sentence VARCHAR(255),
            sentiment FLOAT(3),
            magnitude FLOAT(3)
        )
        """
    )

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        sentence_text = sentence.text.content
        sum_score += sentence_sentiment
        sys.stdout.write('Sentence {} has a sentiment score of {}'.format(sentence_text, sentence_sentiment))
        sys.stdout.flush()
    
    sys.stdout.write('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    sys.stdout.flush()
    
    conn.close()

    return text, sum_score >= 0