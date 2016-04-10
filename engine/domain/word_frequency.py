import pickle

# An ordered dictionary that keeps words in a list indexable by frequency
from collections import OrderedDict


def read_file_ordered_by_frequency():
    with open("resources\kilgarrif_frequency.txt") as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]

            yield freq, word, pos

def read_file_ordered_by_alphabet():
    with open("resources\kilgarrif_alphabetical.txt") as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]

            yield freq, word, pos


def similar_freq_words(word, pos=""):
    # Find frequency of the word
    word_frequency = get_word_frequency((word, pos))
    # Todo: Find better word_frequency system
    if word_frequency == None:
        raise KeyError
    words_by_frequency_table = build_words_by_frequency_table()
    similar_frequency_words = []
    n = 1
    result = []
    while len(result) < 20:
        n *= 2
        for freq in range(word_frequency-n, word_frequency+n+1):
            if freq in words_by_frequency_table:
                similar_frequency_words += words_by_frequency_table[freq]
        # Filter out repetitions, parts of different speech, and same words as target
        if pos in ["a", "n", "v"]:
            result = set([w for (w, p) in similar_frequency_words if w != word and p == pos])
        else:
            result = set([w for (w, p) in similar_frequency_words if w != word])
    return result
    # Find words that have similar frequency

def build_words_by_frequency_table():
    filename = "words_by_frequency_table.p"
    try:
        words_by_frequency_table = pickle.load(open(filename, "rb"))
    except FileNotFoundError as e:
        words_by_frequency_table = OrderedDict()
        for i, (frequency, word, pos) in enumerate(read_file_ordered_by_frequency()):
            # Convert text frequency data into an int
            frequency = int(frequency)
            # Build the frequency dictionary using frequency as the key
            if words_by_frequency_table.get(frequency):
                words_by_frequency_table[frequency].append((word, pos))
            else:
                words_by_frequency_table[frequency] = [(word, pos)]
    return words_by_frequency_table

def build_word_frequency_table():
    filename = "word_frequency_table.p"
    try:
        word_frequency_table = pickle.load(open(filename, "rb"))
    except FileNotFoundError as e:
        # Found through analysis of the file
        # Code at the bottom of the file
        max = 6187267
        min = 800
        word_frequency_table = {}
        for freq, word, pos in read_file_ordered_by_alphabet():
            freq = int(freq)
            word_frequency_table[(word, pos)] = freq
        pickle.dump(word_frequency_table, open(filename, "wb"))
    return word_frequency_table

def get_word_frequency(word):
    word_frequency_table = build_word_frequency_table()
    if word[1] in ["a", "n", "v"]:
        return word_frequency_table.get(word)
    else:
        i = 0
        sum = 0
        for p in ["a", "n", "v"]:
            if (word[0], p) in word_frequency_table:
                sum += word_frequency_table[(word[0], p)]
                i += 1
        if i != 0:
            return int(sum / i)
        else:
            print("word not found")



if __name__ == "__main__":
    print(similar_freq_words("anger", "s"))
    # print(build_word_frequency_table())

    # print(word_frequency_table)



# Read kilgarrif file & normalize the data
# First - found the Max and Min
# frequences = []
# for i, (frequency, word, pos) in enumerate(read_file("kilgarrif_frequency.txt")):
#     frequencies.append(int(frequency))
#
# max = max(frequencies)
# min = min(frequencies)
# print("Max: {}, Min: {}".format(max, min))
#
# >>> Max: 6187267, Min: 800

# Tried normalizing, but there's too much variance to do that
# Will have to enter the data raw

# Using ordered dictionary will help



# Build an ordered word-frequency database

#
# word_frequencies = OrderedDict()
# for i, (frequency, word, pos) in enumerate(read_file("kilgarrif_frequency.txt")):
#     # Convert text frequency data into an int
#     frequency = int(frequency)
#     # Normalize the frequency
#     # Build the frequency dictionary using frequency as the key
#     if word_frequencies.get(frequency):
#         word_frequencies[frequency].append(word)
#     else:
#         word_frequencies[frequency] = [word]

#pickle.dump(word_frequencies, open("kilgarrif-frequency.p", "wb")).close()