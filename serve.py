import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

negative_words_path = "data/negative_words_fr.csv"

def is_text_polite(text):
    tokens = word_tokenize(text, language='french')
    useful_tokens = [token for token in tokens if token not in stopwords.words('french')]
    neg_words = pd.read_csv(negative_words_path)
    for token in useful_tokens:
        if token in neg_words['Word'].values:
            return False
    return True