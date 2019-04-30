import pandas as pd
import fr_core_news_sm
import hunspell

negative_words_path = "data/negative_words_fr.csv"
fr_dict_path = "data/fr-classique.dic"
fr_aff_path = "data/fr-classique.aff"

def is_text_polite(text):
    sp = fr_core_news_sm.load()
    tokens = sp(text)
    #useful_tokens = [token for token in tokens if token not in stopwords.words('french')]

    #neg_words = pd.read_csv(negative_words_path)
    polite = True
    corrected_tokens = []

    hobj = hunspell.Hunspell(fr_dict_path, fr_aff_path)

    for token in tokens:
        word = token.text.lower()
        corrected_tokens.append(word if hobj.spell(word) else hobj.suggest(word)[0])
        #if word in neg_words['Word'].values:
            #polite = False
    return corrected_tokens, polite