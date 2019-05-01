import fr_core_news_sm
from symspellpy.symspellpy import SymSpell, Verbosity

class NLPutils:
    def __init__(self, fr_dict_path):
        self.spacy_model = fr_core_news_sm.load()

        max_edit_distance_dictionary = 2
        prefix_length = 7
        self.sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
        
        term_index = 0
        count_index = 1
        
        self.sym_spell.load_dictionary(fr_dict_path, term_index, count_index)
    
