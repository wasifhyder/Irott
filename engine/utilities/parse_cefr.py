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
    for filename in ["a1", "a2", "b1", "b2", "c1", "c2"]:
        for i, (word, cefr) in enumerate(read_file(filename+ "-vocab.txt")):
            if word not in vocab_model:
                vocab_list[word] = cefr


    for word in sorted(vocab_list.keys()):
        print("{:15} | {}".format(word, vocab_list[word]))
