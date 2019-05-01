import pandas as pd
import fr_core_news_sm
from symspellpy.symspellpy import SymSpell, Verbosity

negative_words_path = "data/negative_words_fr.csv"
fr_dict_path = "data/fr_full.txt"

def is_text_polite(text):
    sp = fr_core_news_sm.load()
    tokens = sp(text)
    #useful_tokens = [token for token in tokens if token not in stopwords.words('french')]

    #neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []
    
    max_edit_distance_dictionary = 2
    prefix_length = 7
    
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)

    term_index = 0
    count_index = 1

    sym_spell.create_dictionary(fr_dict_path, term_index, count_index)

    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST    

    for token in tokens:
        word = token.text.lower()
        suggestions = sym_spell.lookup(word, suggestion_verbosity, max_edit_distance_lookup)
        corrected_tokens.append(word if len(suggestions) < 1 else suggestions[0].term)
        #if word in neg_words['Word'].values:
            #polite = False
    return corrected_tokens, polite