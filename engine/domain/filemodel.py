import word_frequency
from word_lists import word_list, find_cefr
from collections import namedtuple
import datamodel
import ast

class Word:
    # The domain model should be indexable using the word
    # The domain model should be indexable using the word_id
    def __init__(self, word, cefr, senses):
        self.word = word
        self.cefr = cefr
        self.senses = senses

    # Iteration
    def __iter__(self):
        return self.senses.__iter__()
    def __next__(self):
        return self.__next__()

    # Orderable
    def __lt__(self, other):
        if self.word == other.word:
            return self.cefr < other.cefr
        else:
            return self.word < other.word

    # Hashing
    def __eq__(self, other):
        return self.word == other.word
    def __hash__(self):
        return hash(self.word)

    # Representation
    def __repr__(self):
        result = "<Word {}>\n".format((self.word, self.cefr))
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
        pass
    def __hash__(self):
        pass
    def __eq__(self, other):
        pass


class DomainModel:
    def __init__(self, filename):
        self.word_list = {}
        W = namedtuple('Word', 'word cefr senses')
        S = namedtuple('Sense', 'name, pos, definition, examples, synonyms, antonyms, frequency')
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                w = W._make(line.strip().split('||'))
                word = w.word
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
                    frequency = int(s.frequency)
                    s = Sense(name, pos, definition, examples, synonyms, antonyms, frequency)
                    senses.append(s)
                w = Word(word, cefr, senses)
                self.word_list[word] = w

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
            print(s.wordnet_name, s.pos, s.definition, s.examples, s.synonyms, s.antonyms,
                  word_frequency.get_word_frequency(word), sep='||')


if __name__ == "__main__":
    d = DomainModel('resources/data.in')
    for i, word in enumerate(d):
        if i > 10:
            break
        print(word)