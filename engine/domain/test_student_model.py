import pickle
from wordnetapi import Word
import operator
import collections

# old
# domain_model = pickle.load(open("vocab_model.p", "rb"))

# new
domain_model = pickle.load(open("vocab_cefr_list.p", "rb"))


# Loads the student model from a pickle file
student_model = pickle.load(open("empty_student_model-wordnet.p", "rb"))

class Student:
    def __init__(self, name):
        self.name = name
        self.vocabulary_profile = {}

    def initialize_vocabulary_profile(self):
        pass

if __name__ == "__main__":
    # Creates an empty student model
    # student_model = {}
    # for word in sorted(domain_model):
    #     word = domain_model[word]
    #     for definition in word.definitions:
    #         student_model[(word, definition)] = 0.0

    # new
    student_model = {}
    for word in sorted(domain_model):
        # for definition in word.definitions:
        student_model[(word, domain_model[word])] = 0.0

    # Saves the student model into a pickle file
    #pickle.dump(student_model, open("empty_student_model-wordnet.p", "wb"))

    # Loads the student model from a pickle file
    # student_model = pickle.load(open("empty_student_model.p", "rb"))

    for item in sorted(student_model):
        print("{} {}".format(student_model[item], str(item)))
