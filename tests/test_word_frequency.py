import unittest
import nose

from word_frequency import get_word_frequency
from word_frequency import _word_frequency_table
from word_lists import word_list

class wordFrequencyTableTest(unittest.TestCase):
    def testHasWordInTable(self):
        self.assertTrue("rage" in _word_frequency_table)

    # def testHasAllWordsFromWordList(self):
    #     for word in word_list:
    #         if word in _word_frequency_table:
    #             print(word)
    #     self.assertTrue(False)
    #     self.assertTrue(word in _word_frequency_table)

class getWordFrequencyTest(unittest.TestCase):
    def testReturnsNumber(self):
        # Works with part of speech info
        self.assertIsInstance(get_word_frequency("funny", "n"), int)
        self.assertIsInstance(get_word_frequency("funny", "v"), int)
    def testWorksWithoutPartOfSpeechInfo(self):
        # Works without part of speech info
        self.assertIsInstance(get_word_frequency("funny"), int)
    def testWorksWithWrongPartOfSpeechInfo(self):
        # Works with wrong part of speech info
        self.assertIsInstance(get_word_frequency("funny", "a"), int)
        self.assertIsInstance(get_word_frequency("funny", "s"), int)
        self.assertIsInstance(get_word_frequency("funny", "d"), int)
    def testWorksWhenWordIsntPresent(self):
        # Works when word isn't present
        self.assertIsInstance(get_word_frequency("bingobango", pos="v"), int)
        self.assertIsInstance(get_word_frequency("bingobango", pos="d"), int)
        self.assertIsInstance(get_word_frequency("bingobango"), int)


if __name__ == '__main__':
    unittest.main()