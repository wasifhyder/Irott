import pickle
import nltk.data

from WordModel import Word

def read_file(filename):
    with open(filename) as f:
        for line in f.readlines():
            l = line.strip().split()
            word = l[0]
            cefr = l[-1]

            yield word, cefr

vocab_list = {}
vocab_model = {}

if __name__ == "__main__":
    # for filename in ["a1", "a2", "b1", "b2", "c1", "c2"]:
    # for filename in ["a1"]:
    #     for i, (word, cefr) in enumerate(read_vocab_file(filename+"-vocab.txt")):
    #         if word not in vocab_model:
    #             vocab_model[word] = Word(word, cefr)
    #             # vocab_model[word].get_info_from_wordsapi()
    #             #print(vocab_model[word])
    #             #print(vocab_model[word].definitions)
    # for word in sorted(vocab_model.keys()):
    #     print("{:15} | {}".format(word, vocab_model[word].definitions))

    for filename in ["a1", "a2", "b1", "b2", "c1", "c2"]:
        for i, (word, cefr) in enumerate(read_file(filename+ "-vocab.txt")):
            if word not in vocab_model:
                vocab_list[word] = cefr


    for word in sorted(vocab_list.keys()):
        print("{:15} | {}".format(word, vocab_list[word]))

    # pickle.dump(vocab_list, open("vocab_cefr_list.p", "wb"))
    #
    # for word in sorted(vocab_model.keys()):
    #     print("{:15} | {}".format(word, vocab_model[word].definitions))
    #
    #pickle.dump(vocab_model, open("vocab_model_wordnett.p", "wb")).close()
    #
    # if __name__ == "__main__":
    #     vocab_model = pickle.load(open("vocab_model_wordnet.p", "rb"))
    #     for word in sorted(vocab_model.keys()):
    #         if vocab_model[word].cefr == "A1":
    #             print("{:10} {}".format(word, vocab_model[word].definitions))

    # Display a certain CEFR level from vocab_cefr_list.p
    # if __name__ == "__main__":
    #     vocab_model = pickle.load(open("vocab_cefr_list.p", "rb"))
    #     for word in sorted(vocab_list.keys()):
    #         if vocab_list[word] == "C1":
    #             print("{:15} {}".format(word, vocab_list[word]))