import word_frequency
from word_lists import word_list, find_cefr
from collections import namedtuple
import datamodel
import ast

class Word:
    def __init__(self, word, cefr, senses):
        self.word = word
        self.frequency = word_frequency.get_word_frequency(word)
        self.cefr = cefr
        self.senses = {s.name:s for s in senses}

    # Iteration
    def __iter__(self):
        return self.senses.values().__iter__()
    def __next__(self):
        return self.__next__()

    # Orderable
    def __lt__(self, other):
        if isinstance(self, type(other)) and self.word == other.word:
            return self.cefr < other.cefr
        else:
            return self.word < other.word

    # Hashing
    def __eq__(self, other):
        if isinstance(self, type(other)): return self.word == other.word
        return False
    def __hash__(self):
        return hash(self.word)
    # Use senses' name to check
    def __getitem__(self, item):
        return self.senses.__getitem__(item)
    def __contains__(self, item):
        return item in self.senses

    # Representation
    def __repr__(self):
        result = "<Word {}>\n".format((self.word, self.cefr, self.frequency))
        for sense in self:
            result += "\t{}\n".format(sense)
        return result
class Sense:
    def __init__(self, name, pos, definition, examples, synonyms, antonyms, frequency):
        self.name = name
        self.pos = pos
        self.definition = definition
        self.examples = examples
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.frequency = frequency

    def __repr__(self):
        return "<Sense {}>".format((self.name, self.pos,
                                    self.definition, self.examples,
                                    self.synonyms, self.antonyms,
                                    self.frequency))

    def __lt__(self, other):
        if isinstance(self, type(other)): return self.name < other.name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(self, type(other)): return self.name == other.name
        return False


class DomainModel:
    def __init__(self, filename='resources/data.in'):
        self.word_list = {}
        W = namedtuple('Word', 'word cefr senses')
        S = namedtuple('Sense', 'name, pos, definition, examples, synonyms, antonyms')
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                w = W._make(line.strip().split('||'))
                word = w.word
                frequency = word_frequency.get_word_frequency(word)
                cefr = w.cefr
                senses = []
                for i in range(int(w.senses)):
                    line = f.readline()
                    s = (S._make(line.strip().split('||')))
                    name = s.name
                    pos = s.pos
                    definition = s.definition
                    examples = ast.literal_eval(s.examples)
                    synonyms = ast.literal_eval(s.synonyms)
                    antonyms = ast.literal_eval(s.antonyms)
                    frequency = word_frequency.get_word_frequency(word, pos)
                    s = Sense(name, pos, definition, examples, synonyms, antonyms, frequency)
                    senses.append(s)
                w = Word(word, cefr, senses)
                self.word_list[word] = w

    def filter(self, cefr=None):
        if cefr:
            return filter(lambda word: word.cefr == cefr, self)
        return []

    def __iter__(self):
        return self.word_list.values().__iter__()
    def __next__(self):
        return self.__next__()
    def __getitem__(self, item):
        return self.word_list.__getitem__(item)
    def __contains__(self, item):
        return item in self.word_list

def print_info():
    for word in word_list:
        # CSV format
        # Word -
        # Word,CEFR,Num_Senses
        # Senses -
        # name, pos, definition, examples, synonyms, antonyms
        # Followed by that many lines of senses
        w = datamodel.Word(word)
        print(word, find_cefr(word), len(w.senses), sep="||")
        for s in w:
            print(s.wordnet_name, s.pos, s.definition, s.examples,
                  s.synonyms, s.antonyms, sep='||')


if __name__ == "__main__":
    # print_info()
    d = DomainModel()
    # for i, word in enumerate(d):
    #     if i > 10:
    #         break
    #     print(word)