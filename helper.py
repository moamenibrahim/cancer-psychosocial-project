def lexical_diversity(my_text_data):
        word_count = len(my_text_data)
        vocab_size = len(set(my_text_data))
        return(vocab_size/word_count)

def plural(word):
    if word.endswith('y'):
        return(word[:-1] + 'ies')
    elif word[-1] in 'sx' or word[-2:] in ['sh','ch']:
        return(word + 'es')
    elif word.endswith('an'):
        return(word[:-2] + 'en')
    else:
        return(word + 's')

punctuations = ['(',')',';',':','[',']',',','.','\'']
