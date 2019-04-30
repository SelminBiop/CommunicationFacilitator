import pandas as pd
import fr_core_news_sm

negative_words_path = "data/negative_words_fr.csv"

def is_text_polite(text):
    sp = fr_core_news_sm.load()
    tokens = sp(text)
    #useful_tokens = [token for token in tokens if token not in stopwords.words('french')]

    neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []

    for token in tokens:
        word = token.text
        corrected_tokens.append(word)
        if word in neg_words['Word'].values:
            polite = False
    return corrected_tokens, polite