import pickle
import json
import random
from collections import namedtuple

# old
# domain_model = pickle.load(open("vocab_model.p", "rb"))

# new
from test_domain_model import load_word_list_with_wordnet_info, word_list
from WordModel import Word, Sense

# domain_model = pickle.load(open("resources/vocab_cefr_list.p", "rb"))


# Loads the student model from a pickle file
# student_model = pickle.load(open("resources/empty_student_model-wordnet.p", "rb"))

class WordProfile:
    # Word profile is made up of all the word senses
    # Each sense has an individual score associated with it
    # There's an overall word score as well
    def __init__(self, word):
        self.word = Word(word)
        self.total_score = 0.0

        self.senses_profiles = []
        for sense in self.word:
            self.senses_profiles.append(SenseProfile(sense, self))

        self.n = len(self.senses_profiles)

    def __iter__(self):
        return self.senses_profiles.__iter__()
    def __next__(self):
        return self.senses_profiles.__next__()

    def __eq__(self, other):
        return self.word.word == self.other.word and self.word.cefr == self.other.cefr

    def __hash__(self):
        return self.word.__hash__()

    def __repr__(self):
        result = ""
        result += "The word profile for {} is {:.4f}: \n\t".format(self.word, self.total_score)
        for sense_profile in self.senses_profiles:
            result += str(sense_profile) + '\n\t'
        return result
    # Total Score is the average of all sense scores

    def update_score(self):
        self.total_score = (sum([x.score for x in self.senses_profiles])/self.n)

class SenseProfile:
    # Sense profile is an individual sense
    # A question is generated based on the word sense
    # A score is given based on the word sense
    # Each sense has an associated history of questions that have been asked
    def __init__(self, sense, parent):
        self.parent = parent
        self.sense = sense
        self.score = 0.0

    def __repr__(self):
        return "{}".format((self.sense, self.score))

    def __eq__(self, other):
            return self.sense == other.sense

    def __hash__(self):
        return hash((self.sense))
    # Update Score for the sense

    def update_score(self, correct):
        if correct:
            self.score += 0.2
        else:
            self.score -= 0.2
        self.parent.update_score()

class Student:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.vocabulary_profile = {}
        for word in word_list:
            self.vocabulary_profile[word] = WordProfile(word)

    def initialize_vocabulary_profile(self):
        # A student's vocabulary profile can be indexed using the word profile
        # Each word has multiple senses, each with their own profile
        for word in load_word_list_with_wordnet_info():
            word_profile = WordProfile(word)
            self.vocabulary_profile

    def get_word_profile(self, word):
        return self.vocabulary_profile[word]

    def get_sense_profile(self, sense):
        return self.get_word_profile(sense.parent_word.word).senses_profiles

    def update_score(self, sense, correct):
        # Find the sense
        sense_profiles = self.get_sense_profile(sense)
        for s in sense_profiles:
            if s.sense == sense:
                s.update_score(correct)
                break


if __name__ == "__main__":
    wasif = Student("wasif", "pass")
    sense = Word("pool").senses[0]
    wasif.update_score(sense, correct=True)
    sense = Word("fight").senses[0]
    wasif.update_score(sense, correct=True)
    sense = Word("age").senses[0]
    wasif.update_score(sense, correct=False)

    print(wasif.get_word_profile('pool'))
    print(wasif.get_word_profile('age'))
    print(wasif.get_word_profile('fight'))



