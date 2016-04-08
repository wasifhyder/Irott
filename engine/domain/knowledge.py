from nltk.corpus import wordnet as wn


def give_definition(word):
    syns = wn.synsets(word)
    for d in syns:
        print(d.name(), d.lemma_names(), d.definition(), sep="\n")
        for example in d.examples():
            print("---", example)
        print()

def definition(word):
    for i, j in enumerate(wn.synsets(word)):
        print("Meaning", i, "NLTK ID:", j.lemma_names())
        print("Definition:", j.definition())

def thesaurus(word):
    for i, j in enumerate(wn.synsets(word)):
        print("Meaning", i, "NLTK ID:", j.name())
        print("Definition:", j.definition())
        print("Synonyms:", ", ".join(j.lemma_names()))
        print("Antonyms:", ", ".join(j.antonyms()) if j.antonyms() else "")

if __name__ == "__main__":
    f = open("d2-vocab.txt")
    for i in range(1):
        word = "Gray"
        print(word)
        print("-"*15)
        thesaurus(word)
        print("-"*15)

