import json
import fr_core_news_sm
from symspellpy.symspellpy import SymSpell
from flask import Flask, request
from serve import is_text_polite

class FlaskApp(Flask):

    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.spacy_model = fr_core_news_sm.load()

        #max_edit_distance_dictionary = 2
        #prefix_length = 7
        #self.sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
        
        #term_index = 0
        #count_index = 1
        
        #self.sym_spell.load_dictionary("data/fr_full.txt", term_index, count_index)


app = FlaskApp(__name__)
app.config['DEBUG'] = True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    input_data = request.json
    text_to_evaluate = input_data["text"]

    corrected_text, is_polite = is_text_polite(text_to_evaluate)

    output_data = {
        "is_polite":is_polite,
        "corrected_text":corrected_text
    }
    response = json.dumps(output_data, ensure_ascii=False)

    return response
