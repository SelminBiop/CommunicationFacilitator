from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import os

client = language.LanguageServiceClient()
db_url = os.environ['DATABASE_URL']

def is_text_polite(text):    

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        sys.stdout.write('Sentence {} has a sentiment score of {}'.format(sentence.text, sentence_sentiment))
        sys.stdout.flush()
    
    sys.stdout.write('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    sys.stdout.flush()
        
    return text, score >= 0