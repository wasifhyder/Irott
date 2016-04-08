from nltk.corpus import wordnet as wn

class Word:
    def __init__(self, word, cefr="UN"):
        self.word = word
        self.cefr = cefr
        self.definitions = [Definition(sense) for sense in wn.synsets(self.word)]

        # if data:
        #     for definition_data in data:
        #         self.definitions.append(Definition(definition_data))

    def __repr__(self):
        return "<Word: {:12}>".format(self.word)

class Definition:
    def __init__(self, sense):
        self.partOfSpeech = sense.pos()
        self.definition = sense.definition()
        self.examples = sense.definition()
        self.synonyms = synonyms(sense)
        self.antonyms = antonyms(sense)
        self.hyperym = sense.hypernyms()
        self.homonym = sense.hyponyms()

    def __repr__(self):
        return "{}".format(self.definition)

def antonyms(sense):
    result = []
    for lemma in sense.lemmas():
        ants = lemma.antonyms()
        for ant in ants:
            result.append(ant.synset())
        # for ant in ants:
        #     result += ant.name()
    return result

def synonyms(sense):
    result = []
    for lemma in sense.lemmas():
        result.append(lemma.synset())
    return result


if __name__ == "__main__":
    # rage = Word("anything")
    # rage.get_info_from_wordsapi()
    # print(rage.definitions)
    # pass
    w = Word("rage")
    print(w.definitions)
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