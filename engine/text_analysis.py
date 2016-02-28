# The purpose of this code functionality would be to analyze a written text provided by the user of the
# environmnet that is being built. Identifying key qualities of the documents would be a step in providing
# analysis.

import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn

if __name__ == "__main__":
    nltk.download()
    with open("essay.txt", "r", encoding="utf-8") as essay:
        tokens = \
            word_tokenize(" ".join(essay.readlines()))