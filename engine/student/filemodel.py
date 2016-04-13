import random
from collections import namedtuple

from ..instructor.accuracy_model import AccuracyModel
from ..domain import filemodel

class WordProfile:
    def __init__(self, word):
        self.word = word
        self.score = 0
        self.sense_profiles = {sense.name:SenseProfile(self, sense) for sense in word}
        self.n = len(self.sense_profiles)

    def update(self):
        if self.n == 0: return 0
        self.score = sum([v.score for x,v in self.sense_profiles.items()])/self.n

    def updateSense(self, sense, correct):
        if isinstance(sense, str):
            return self[sense].update(correct)
        else:
            return self[sense.name].update(correct)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.score == other.score:
                return self.word.cefr < other.word.cefr
            return self.score < other.score
        elif isinstance(other, type(int, float)):
            return self.score < other
        raise TypeError

    def __iter__(self):
        return self.sense_profiles.__iter__()
    def __next__(self):
        return self.__next__()
    def __len__(self):
        return self.sense_profiles.__len__()

    def __getitem__(self, item):
        return self.sense_profiles.__getitem__(item)

    def __repr__(self):
        # return "{}||{}".format(self.word.word, self.score)
        result = "{}||{}||{}\n".format(self.word.word, len(self), self.score)
        for sense_profile in self:
            result += "\t{}\n".format(self[sense_profile])
        return result.rstrip()

class SenseProfile:
    def __init__(self, parent, sense):
        self.parent = parent
        self.sense = sense
        self.name = sense.name
        self.score = 0.0
        self.proficiency = AccuracyModel()

    def update(self, correct):
        self.score = self.proficiency.update(correct)
        self.parent.update()

    def __repr__(self):
        return "{}||{}".format(self.sense.name, self.score)

class VocabularyProfile:
    def __init__(self):
        # Based on word: wordprofile
        self.profile = {}

        d = filemodel.DomainModel()
        for word_name, word_model in d.items():
            self.profile[word_name] = WordProfile(word_model)
        pass

    def __getitem__(self, item):
        return self.profile[item]
    def items(self):
        return self.profile.items()
    def __iter__(self):
        return self.profile.__iter__()
    def __next__(self):
        return self.profile.__next__()

    def load(self, f):
        # d = filemodel.DomainModel()
        WP = namedtuple('WordProfile', 'word senses score')
        SP = namedtuple('SenseProfile', 'sense score')
        while True:
            line = f.readline()
            if line == '': break
            wp = WP._make(line.strip().split('||'))
            word = wp.word
            senses = int(wp.senses)
            word_score = float(wp.score)
            self.profile[word].score = word_score
            for i in range(senses):
                line = f.readline()
                sp = SP._make(line.strip().split('||'))
                sense = sp.sense
                sense_score = float(sp.score)
                self.profile[word][sense].score = sense_score
            self.profile[word].update()

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

    def __repr__(self):
        result = ''
        for _, word_profile in self.items():
            result += '{}\n'.format(word_profile)
        return result


class StudentModel:
    def __init__(self, username, password, new=False):
        self.username = username
        self.password = password
        self.vocabulary_profile = VocabularyProfile()
        if new:
            self.save()
        else:
            self.load()

    def __repr__(self):
        result = '{}||{}\n'.format(self.username, self.password)
        result += self.vocabulary_profile.__repr__()
        return result

    def __getattr__(self, item):
        return self.vocabulary_profile.__getattribute__(item)

    def load(self):
        filename = "userfiles/{}-{}-model.in".format(self.username, self.password)

        with open(filename, 'r') as f:
            _ = f.readline()
            self.vocabulary_profile.load(f)


    def save(self):
        filename = "userfiles/{}-{}-model.in".format(self.username, self.password)
        with open(filename, 'w') as f:
            f.write(self.__repr__())

    def __getitem__(self, item):
        return self.vocabulary_profile[item]

    def __getattr__(self, item):
        return self.vocabulary_profile.__getattribute__(item)

def print_info():
    # VocabularyProfile()
    # d = filemodel.DomainModel()
    # print('Username', 'Pass')
    # for word in random.sample(list(d), 1):
    #     wp = WordProfile(word)
    #     print(wp.word.word, wp.score, sep='||')
    #     for sp in wp:
    #         print(sp, wp[sp], sep='||')
    s = StudentModel('wasif', '123')
    s['cello']['cello.n.01'].update(True)
    print(s['cello'])
    s.save()

if __name__ == "__main__":
    # print_info()
    # d = filemodel.DomainModel()
    # # for word in random.sample(list(d), 1):
    # for word in [d["rage"]]:
    #     wp = WordProfile(word)
    #     for i in range(8):
    #         s = random.choice(word)
    #         wp.updateSense(s, False)
    # wp.updateSense(s, True)
    # print(wp)
    s = StudentModel('wasif', '123')
    print(s['cello'])
    pass
