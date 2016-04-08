import random

from nltk.corpus import wordnet as wn

class Word:
    def __init__(self, word, cefr="UN"):
        self.word = word
        self.cefr = cefr
        self.senses = [Sense(sense) for sense in wn.synsets(self.word)]


    def __repr__(self):
        return "<Word: {:12}>".format(self.word)

class Sense:
    def __init__(self, sense):
        self.word = sense.name().split('.')[0]
        self.sense = sense
        self.wordnet_name = sense.name()
        self.pos = sense.pos()
        self.definition = sense.definition()
        self.examples = sense.examples()

        self.synonyms = self.get_synonyms()
        self.antonyms = self.get_antonyms()
        self.hypernyms = []
        self.homonyms = []
        self.frequency = []

    def __repr__(self):
        return "S: {}".format(self.wordnet_name)

    def list_everything(self):
        print("Name: {}\n"
              "POS: {}\n"
              "Definition: {}\n"
              "Examples: {}\n"
              "Synonyms: {}\n"
              "Antonyms: {}\n"
              "Hypernym: {}\n"
              "Homonyms: {}"
            .format(
            self.wordnet_name,
            self.pos,
            self.definition,
            self.examples,
            self.synonyms,
            self.antonyms,
            self.hypernyms,
            self.homonyms,
        ))
        # print("Lemmas: {}\n".format([Sense(l) for l in self.sense.lemmas()]))

    def get_synonyms(self):
        """ Tried very hard to embed synset information
            However, the lemmas don't have an associated synset information to save

            One solution would be to calculate synsets based on similarity
        """
        result = []
        # Find the original synset from which this sense came
        # The Sense class initializes based on the information provided by a synset
        wordnet_sense = next(x for x in wn.synsets(self.word) if x.name() == self.wordnet_name)
        for lemma in wordnet_sense.lemmas():
            result.append(lemma.name())
        result.remove(self.word)
        return result

    def get_antonyms(self):
        result = []
        # Find the original synset from which this sense came
        wordnet_sense = next(x for x in wn.synsets(self.word) if x.name() == self.wordnet_name)
        for lemma in wordnet_sense.lemmas():
            result += (x.name() for x in lemma.antonyms())
        # result.remove(self.word)
        return result




if __name__ == "__main__":
    # rage = Word("anything")
    # rage.get_info_from_wordsapi()
    # print(rage.definitions)
    # pass
    # w = Word("rage")
    from nltk.corpus import wordnet as wn
    w = Word("calm")
    sense = w.senses[0]
    # This would have been a disambiguation technique
    # wouldn't work because the word has no information besides itself
    for word in sense.synonyms:
        print(word, [x for x in Word(word).senses])
        # sense.list_everything()
    # for sense in wn.synsets("good"):
    #     print("Sense: {}\n"
    #           "Part of Speech: {}\n"
    #           "Definition: {}\n"
    #           "Examples: {}\n"
    #           "Synonyms: {}\n"
    #           "Antonyms: {}\n"
    #           "Hypernyms: {}\n"
    #           "Hyponyms: {}\n"
    #           "-------------------------------------"
    #           .format(sense.lemmas()[0].name(), sense.pos(), sense.definition(), sense.examples(), synonyms(sense), antonyms(sense),
    #                   sense.hypernyms(), sense.hyponyms()))