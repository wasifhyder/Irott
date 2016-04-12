import random

from domain import filemodel

class WordProfile:
    def __init__(self, word):
        self.word = word

class VocabularyProfile:
    def __init__(self):
        # Based on word: score format
        self.profile = {}


class StudentModel:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.vocabulary_profile = VocabularyProfile()


# Student Model
# Name, Pass
# <Begin Word Profile>
# word score
#     sense score
#     sense score
# <End Word Profile>

if __name__ == "__main__":
    d = filemodel.DomainModel()
    for word in random.sample(list(d), 3):
        print(word)