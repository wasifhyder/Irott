import json
import random
from collections import namedtuple
import os.path

from engine.instructor.accuracy_model import AccuracyModel
from engine.domain import filemodel

class WordProfile:
    def __init__(self, word, score, sense_profiles, active, date_activated):
        self.word = word
        self.score = score
        self.sense_profiles = {s:SenseProfile.load_json(word, sp) for s, sp in sense_profiles.items()}
        self.active = active
        self.date_activated = date_activated
        self.n = len(self.sense_profiles)

    @staticmethod
    def load_json(word_profile):
        word = word_profile['word']
        score = word_profile['score']
        sense_profiles_json = word_profile['sense_profile']
        active = word_profile['active']
        date_activated = word_profile['date_activated']
        return WordProfile(word, score, sense_profiles_json, active, date_activated)

    def update(self):
        if self.n == 0: return 0
        self.score = sum([v.score for x,v in self.sense_profiles.items()])/self.n
    def updateSense(self, sense, correct):
        if isinstance(sense, str):
            self[sense].update(correct)
        else:
            self[sense.name].update(correct)
        self.update()
    # Ordering
    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.score == other.score:
                return self.word.cefr < other.word.cefr
            return self.score < other.score
        elif isinstance(other, type(int, float)):
            return self.score < other
        raise TypeError
    # Iteration
    def __iter__(self):
        return self.sense_profiles.__iter__()
    def __next__(self):
        return self.__next__()
    def __len__(self):
        return self.sense_profiles.__len__()
    # Representation
    def dict_repr(self):
        result = {
            "word": self.word,
            "score": self.score,
            "sense_profile": {
                name: sense_profile.dict_repr() for name, sense_profile in self.sense_profiles.items()
                },
            "active": self.active,
            "date_activated": self.date_activated
        }
        return result
    def __getitem__(self, item):
        return self.sense_profiles.__getitem__(item)
    def __repr__(self):
        result = "{}||{}||{}\n".format(self.word, len(self), self.score)
        for sense_profile in self:
            result += "\t{}\n".format(self[sense_profile])
        return result.rstrip()


class SenseProfile:
    def __init__(self, word, name, score, answer_history):
        self.word = word
        self.name = name
        self.score = score
        self.proficiency = AccuracyModel(answer_history=answer_history)

    # Load object from json representation
    @staticmethod
    def load_json(w, sp):
        word = w
        name = sp['name']
        score = sp['score']
        answer_history = eval(sp['answer_history'])
        return SenseProfile(word, name, score, answer_history)
    # Update the score given the next correct/incorrect answer
    def update(self, correct):
        self.score = self.proficiency.update(correct)
    # Representation
    def dict_repr(self):
        result = {
            'name': self.name,
            'score': self.score,
            'answer_history': self.proficiency.__repr__()
        }
        return result
    def __repr__(self):
        return "{}||{}".format(self.name, self.score)


class VocabularyProfile:
    def __init__(self):
        # Based on word: wordprofile
        self.profile = {}
        #
        # d = filemodel.DomainModel()
        # for word_name, word_model in d.items():
        #     self.profile[word_name] = WordProfile(word_model)
        # pass

    def __getitem__(self, item):
        return self.profile[item]
    def items(self):
        return self.profile.items()
    def __iter__(self):
        return self.profile.__iter__()
    def __next__(self):
        return self.profile.__next__()

    def load_json(self, f, new=False):
        if new == False:
            vocabulary_profile = f['vocabulary_profile']
        else:
            vocabulary_profile = f
        for word, word_profile in vocabulary_profile.items():
            self.profile[word] = WordProfile.load_json(word_profile)

    # Words Lists
    def words(self, n=1, f=None):
        result = []
        i = 0
        for word in filter(f, self):
            if i > n: break
            result.append(word)
            i += 1
        return result
    def wordsSeen(self, n=1):
        return self.words(n, lambda x: self[x].score != 0)
    def wordsNotSeen(self, n=1):
        return self.words(n, lambda x: self[x].score == 0)
    # Representation
    def dict_repr(self):
        result = {}
        for _, word_profile in self.items():
            result[_] = word_profile.dict_repr()
        return result
    def __repr__(self):
        result = {}
        for _, word_profile in self.items():
            result[_] = word_profile
        return str(result)


class StudentModel:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.vocabulary_profile = VocabularyProfile()
        self.filename = "userfiles/{}-{}-model.txt".format(self.username, self.password)

        if os.path.isfile(self.filename):
            self.load(new=False)
        else:
            new = input("User does not exist. Create a new user? (Y) or (N): ")
            if new.lower() == "y":
                new = True
                self.load(new)
            else:
                new = False
                raise Exception("User does not exist")

    # Loading student model from data, or from scratch
    def load(self, new=False):
        filename = "userfiles/{}-{}-model.txt".format(self.username, self.password)
        if new:
            filename = "userfiles/empty-profile.txt"
        with open(filename, 'r') as f:
            f = json.load(f)
            self.vocabulary_profile.load_json(f, new=new)
        if new:
            self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.dict_repr(), indent=4))

    # Representation
    def dict_repr(self):
        result = {
            'username': self.username,
            'password': self.password,
            'vocabulary_profile': self.vocabulary_profile.dict_repr()
        }
        return result
    def __repr__(self):
        result = '{}||{}\n'.format(self.username, self.password)
        result += self.vocabulary_profile.__repr__()
        return result
    # Item & Attr retrieval - Accesses vocabulary profile
    # Provides API: Student[word] => word_profile
    #               Student.wordsSeen() => words the student has seen
    def __getitem__(self, item):
        return self.vocabulary_profile[item]
    def __getattr__(self, item):
        return self.vocabulary_profile.__getattribute__(item)


if __name__ == "__main__":
    s = StudentModel('empty', '0')
    s.save()
    s.vocabulary_profile['rage']['rage.n.02'].update(True)
    s.vocabulary_profile['rage']['rage.n.02'].update(False)
    s.vocabulary_profile['rage']['rage.n.02'].update(False)
    s.vocabulary_profile['rage']['rage.n.02'].update(True)
    s.vocabulary_profile['rage']['rage.n.02'].update(True)
    print(json.dumps(s.vocabulary_profile['rage'].dict_repr(), indent=4))



