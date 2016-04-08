import pickle
from wordnetapi import Word

domain_model = pickle.load(open("vocab_cefr_list.p", "rb"))

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

# new
def word_def_syn(word):
    if word in domain_model:
        word = Word(word, domain_model[word])
        print(word, word.definitions)

if __name__ == "__main__":
    i = 0
    for word in sorted(domain_model.keys()):
        if i > 25: break
        i += 1
        #word = Word(word, cefr=domain_model[word])
        print(word)
        #print("{} {}".format(word, word.definitions))
    # word_def_syn()