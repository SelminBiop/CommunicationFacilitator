import fr_core_news_sm
import sys
from pattern.fr import sentiment

negative_words_path = "data/negative_words_fr.csv"

sp = fr_core_news_sm.load()

def is_text_polite(text):
    tokens = sp(text)
    useful_tokens = [token for token in tokens if not token.is_stop]
    sentences = list(tokens.sents)

    corrected_tokens = []   

    for token in useful_tokens:
        word = token.lemma_
        corrected_tokens.append(word)

    pol_sum = 0
    for sentence in sentences:
        polarity = sentiment(sentence)[0]
        pol_sum += polarity
        sys.stdout.write(sentence)
        sys.stdout.write(str(polarity))
        sys.stdout.flush()
        
    return corrected_tokens, pol_sum >= 0