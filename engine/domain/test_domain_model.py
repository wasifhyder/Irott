import pickle
from wordnetapi import Word
from collections import namedtuple

def load_word_list():
    word_list = pickle.load(open("vocab_cefr_list.p", "rb"))
    return word_list.keys()

def load_word_cefr_list():
    word_cefr_list = pickle.load(open("vocab_cefr_list.p", "rb"))
    return word_cefr_list

# old
# def word_def_syn(word):
#     word = domain_model[word]
#     print(word.word)
#     for definition in word.definitions:
#         print("-"*15)
#         print(definition)
#         if definition.synonyms:
#             for synonym in definition.synonyms:
#                 print(synonym)

# Don't know what this is for. Most likely, to print word and its definitions
# def word_def_syn(word):
#     if word in word_list:
#         word = Word(word, word_list[word])
#         print(word, word.definitions)

if __name__ == "__main__":
    word_cefr_list = load_word_cefr_list()
    word_list = load_word_list()

    Word = namedtuple('Word', ['word', 'cefr'])
    word_list_tuple = [Word(k,v) for k,v in word_cefr_list.items()]

    t = [(k,v) for k, v in word_cefr_list.items()]

    for item in filter(lambda x: x.cefr=="C1", word_list_tuple):
        print(item.word, item.cefr)

