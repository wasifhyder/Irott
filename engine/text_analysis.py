# The purpose of this code functionality would be to analyze a written text provided by the user of the
# environmnet that is being built. Identifying key qualities of the documents would be a step in providing
# analysis.

import nltk
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import wordnet as wn


if __name__ == "__main__":
    with open("essay.txt", "r", encoding="utf-8") as essay:
        #nltk.download()
        tokens = word_tokenize(" ".join(essay.readlines()))
        count = Counter(tokens)
        print(count)