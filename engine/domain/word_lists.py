import pickle
from datamodel import Word


def load_word_list_with_cefr_info():
    word_cefr_list = pickle.load(open("resources/vocab_cefr_list.p", "rb"))
    word_cefr_list = [(k, v) for k, v in word_cefr_list.items()]
    return word_cefr_list

def load_word_list_with_wordnet_info():
    # List of words created using Word from wordnetapi
    word_cefr_list = pickle.load(open("resources/vocab_cefr_list.p", "rb"))
    word_cefr_list = [Word(k, v) for k, v in word_cefr_list.items()]
    return word_cefr_list

def load_word_list():
    # Redundant
    word_list = [k for k,v in load_word_list_with_cefr_info()]
    return word_list

def load_domain_model():
    vocab_list = []
    for word, cefr in load_word_list_with_cefr_info().items():
        vocab_list.append(Word(word))
    return vocab_list

def load_word_list_by_cefr_key():
    return pickle.load(open("resources/word_list_by_cefr_key.p", 'rb'))

def find_cefr(word):
    for cefr, wordset in load_word_list_by_cefr_key().items():
        if word in wordset:
            return cefr
    return "U0"


word_list = load_word_list()
word_list_by_cefr_key = load_word_list_by_cefr_key()


if __name__ == "__main__":
    print(find_cefr("snake"))