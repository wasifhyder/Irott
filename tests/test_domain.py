import unittest
import mock
import nose

from WordModel import Word, get_senses, Sense
from nltk.corpus import wordnet as wn


class TestGetSenses(unittest.TestCase):
    def setUp(self):
        pass

    # @mock.patch('nltk.corpus.wordnet')
    def testAre(self):
        word = Word("rage")
        self.assertEquals(word.senses, [Sense(sense, parent=word) for sense in wn.synsets("rage")])

class TestWord(unittest.TestCase):
    def setUp(self):
        pass

    def testValidWordHasCEFR(self):
        word = Word("village")
        self.assertTrue(word.cefr == 'A1')

    def testInvalidWordHasCEFR(self):
        word = Word("retributionary")
        self.assertEqual(word.cefr, 'U0')

    def testWordProperty(self):
        word = Word("hate")
        self.assertEquals(word.word, "hate")

class TestSenses(unittest.TestCase):
    def setUp(self):
        pass

    def testSensesEquality(self):
        sense1 = Word("rage").senses[0]
        sense2 = Word("rage").senses[1]
        sense3 = Word("hate").senses[0]
        self.assertEquals(sense1, sense1)
        self.assertEquals(sense2, sense2)
        self.assertEquals(sense3, sense3)
        self.assertNotEquals(sense1, sense2)
        self.assertNotEquals(sense1, sense3)

    def testSensesEqualityHasSeparateTypes(self):
        sense1 = Word("rage").senses[0]
        self.assertNotEquals(sense1, "yalla")

    def testSenseIsOrderablyByWordAndSenseId(self):
        word1 = Word("cage")
        word2 = Word("page")
        word3 = Word("rage")
        sense1 = word1.senses[0]
        sense12 = word1.senses[2]
        sense2 = word2.senses[4]
        sense3 = word3.senses[0]
        self.assertLess(sense1, sense12)
        self.assertLess(sense12, sense3)
        self.assertLess(sense2, sense3)




if __name__ == '__main__':
    unittest.main()