from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import os

client = language.LanguageServiceClient()
db_url = os.environ['DATABASE_URL']

def is_text_polite(text):    

    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document, encodingType=enums.EncodingType.UTF32)

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    sum_score = 0

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        sentence_text = sentence.text.content
        sum_score += sentence_sentiment
        sys.stdout.write('Sentence {} has a sentiment score of {}'.format(sentence_text, sentence_sentiment))
        sys.stdout.flush()
    
    sys.stdout.write('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    sys.stdout.flush()
        
    return text, sum_score >= 0