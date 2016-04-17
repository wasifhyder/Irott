import json
from mongoengine import *
# from pymongo.mongo_client import MongoClient

from engine.domain.word_frequency import get_word_frequency_all, get_word_frequency
from engine.domain.filemodel import DomainModel

# conn = MongoClient()
# FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(format=FORMAT)
# logger = logging.getLogger("humongolus")
# orm.settings(logger=logger, db_connection=conn)

class Frequency(EmbeddedDocument):
    # word = ReferenceField(Word)
    total = IntField(required=True)
    n = IntField(default=0)
    v = IntField(default=0)
    a = IntField(default=0)

    meta = {
        'collection': 'domain',
        'indexes': [
            'word',
            'total',
            'n',
            'v',
            'a',
        ]
    }
CEFR_VALUES = ('A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'U0')


class Sense(EmbeddedDocument):
    meta = {'collection': 'domain'}
    name = StringField(required=True)
    pos = StringField(required=True)
    definition = StringField(required=True)
    examples = ListField(StringField(), default=list)
    synonyms = ListField(StringField(), default=list)
    antonyms = ListField(StringField(), default=list)


class Word(Document):
    word = StringField(required=True)
    cefr = StringField(required=True, choices=CEFR_VALUES)
    frequency = EmbeddedDocumentField(Frequency) # This should be frequency indexed by pos
    senses = ListField(EmbeddedDocumentField(Sense))

    meta = {'collection': 'domain',
            'indexes': [
                'word',
                'cefr',
                'frequency.total',
                'senses.name',
            ],
            'ordering': '+word'
    }



seen = {}
def create_word(word):
    if word in seen:
        return seen[word]

    w = d[word]
    mword = Word()
    mword.word = w.word
    mword.cefr = w.cefr

    # Frequency
    mword_frequencies = get_word_frequency_all(word)
    a, n, v = 0, 0, 0
    for pos in ['a', 'n', 'v']:
        if mword_frequencies != 0 and pos in mword_frequencies:
            if pos == 'a': a = mword_frequencies[pos]
            if pos == 'n': n = mword_frequencies[pos]
            if pos == 'v': v = mword_frequencies[pos]

    mword.frequency = Frequency()
    mword.frequency.total = get_word_frequency(word)
    mword.frequency.n = n
    mword.frequency.v = v
    mword.frequency.a = a
    # Senses
    msenses = []
    for sense in w:
        msense = Sense()
        msense.name = sense.name
        msense.pos = sense.pos
        msense.definition = sense.definition
        msense.examples = sense.examples
        msense.synonyms = sense.synonyms #[create_word(ww) for ww in sense.synonyms]
        msense.antonyms = sense.antonyms #[create_word(ww) for ww in sense.synonyms]
        msenses.append(msense)
    mword.senses = msenses
    seen[word] = mword
    return seen[word]

def create_from_scratch():
    d = DomainModel()
    connect('irott')
    for word in d:
    # w = create_word(word)
        w = create_word(word)
        w.save()
    # print(json.dumps(d[word].json(), indent=4))


