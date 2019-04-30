import pandas as pd
import fr_core_news_sm
from unidecode import unidecode
from symspellpy.symspellpy import SymSpell, Verbosity

negative_words_path = "data/negative_words_fr.csv"
frequency_dict_path = "data/fr_50k.txt"

def is_text_polite(text):
    #tokens = nltk.word_tokenize(text, language='french')
    sp = fr_core_news_sm.load()
    tokens = sp(text)
    #useful_tokens = [token for token in tokens if token not in stopwords.words('french')]

    neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []

    max_edit_distance_dict = 2
    prefix_length = 7

    sym_spell = SymSpell(max_edit_distance_dict, prefix_length)

    term_index = 0
    count_index = 1

    sym_spell.load_dictionary(frequency_dict_path, term_index, count_index)

    suggestion_verbosity = Verbosity.CLOSEST
    max_edit_distance_lookup = 2

    for token in tokens:
        token = unidecode(token.text.lower())
        suggestions = sym_spell.lookup(token, suggestion_verbosity, max_edit_distance_lookup)
        corrected_tokens.append(suggestions[0].term if len(suggestions) > 0 else token)
        if token in neg_words['Word'].values:
            polite = False
    return corrected_tokens, polite