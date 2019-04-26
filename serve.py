import pandas as pd
import sys
from nltk.corpus import stopwords

negative_words_path = "data/negative_words_fr.csv"

def is_text_polite(text):
    #tokens = nltk.word_tokenize(text, language='french')
    tokens = text.split(" ")
    useful_tokens = [token for token in tokens if token not in stopwords.words('french')]
    neg_words = pd.read_csv(negative_words_path)
    print(neg_words.describe())
    print(neg_words.head())
    sys.stdout.flush()
    for token in useful_tokens:
        if token in neg_words['Word'].values:
            return False
    return True