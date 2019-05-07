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
        pol_sum += polarity
        
    return corrected_tokens, pol_sum >= 0