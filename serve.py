import pandas as pd
import fr_core_news_sm
from pattern.fr import sentiment

negative_words_path = "data/negative_words_fr.csv"

sp = fr_core_news_sm.load()

def is_text_polite(text):
    tokens = sp(text)
    useful_tokens = [token for token in tokens if not token.is_stop]

    neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []   

    for token in useful_tokens:
        word = token.lemma_
        corrected_tokens.append(word)
        if word in neg_words['Word'].values:
            polite = False
    return corrected_tokens, polite