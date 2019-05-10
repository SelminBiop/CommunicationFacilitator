from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import psycopg2
import sys
import os

client = language.LanguageServiceClient()
db_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
db_pwd = os.environ['DATABASE_PWD']
db_name = os.environ['DATABASE_NAME']

def is_text_polite(text):    

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document, encoding_type=enums.EncodingType.UTF32)

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    sum_score = 0

    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pwd)
    cur = conn.cursor()

    analyzed_text = []

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        sentence_text = sentence.text.content
        sum_score += sentence_sentiment
        analyzed_text.append((sentence_text, sentence_sentiment))
        cur.execute(
            """
            INSERT INTO sentences (sentence, sentiment, magnitude)
            VALUES(%s, %s, %s)
            """,
            (sentence_text, sentence_sentiment, sentence.sentiment.magnitude)
        ) 
        sys.stdout.write('Sentence {} has a sentiment score of {}'.format(sentence_text, sentence_sentiment))
        sys.stdout.flush()
    
    sys.stdout.write('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    sys.stdout.flush()
    cur.close()
    conn.commit()
    conn.close()

    return analyzed_text, sum_score >= 0