import pandas as pd
import nlputils
from symspellpy.symspellpy import Verbosity

negative_words_path = "data/negative_words_fr.csv"

def is_text_polite(text, nlputils):
    tokens = nlputils.spacy_model(text)
    #useful_tokens = [token for token in tokens if token not in stopwords.words('french')]

    #neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []

    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST    

    for token in tokens:
        word = token.text.lower()
        suggestions = nlputils.sym_spell.lookup(word, suggestion_verbosity, max_edit_distance_lookup)
        corrected_tokens.append(word if len(suggestions) < 1 else suggestions[0].term)
        #if word in neg_words['Word'].values:
            #polite = False
    return corrected_tokens, polite