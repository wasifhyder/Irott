from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy_utils import drop_database

'''
The Domain Model -
This is the model we'll use to collect all the knowledge regarding vocabulary that
we have. This model will be referenced by both the student model and the instructor
model.
'''

import datamodel
from word_lists import word_list

Base = declarative_base()


class Word(Base):
    """
    A word can have:
        Definitions: 1 or more
    """
    __tablename__ = 'word'
    wordid = Column(Integer(), primary_key=True)
    word = Column(String(50), unique=True)
    cefr = Column(String(3))
    word_frequency = Column(Integer())

    senses = relationship("Sense", backref="word")

    def __repr__(self):
        return "<Word {}>".format(self.word)


class Sense(Base):
    """
    Each definition of a word has:
        1. The definition itself
        2. Examples associated with that definition (0 or more)
        3. Synonyms of that definition (0 or more)
        4. Antonyms of that definition (0 or more)
        5. CEFR Level

    Note: In the student model, each student would have a corresponding performance for
          each word definition.
    """
    __tablename__ = 'sense'

    senseid = Column(Integer(), primary_key=True)
    wordid = Column(Integer, ForeignKey('word.wordid'))
    pos = Column(String(3))
    sense = Column(String(50))
    definition = Column(String(50))

    # examples = relationship("Example", backref="definition")
    # synonyms = relationship("Synonym", backref="definition")


    def __repr__(self):
        return "<Definition {}>".format(self.definition)

# class CEFR(Base):
#     __tablename__ = 'cefr'
#
#     id = Column(Integer(), primary_key=True)
#     definition_id = Column(Integer, ForeignKey('definition.id'))
#     cefr = Column(String(12))
#
#     def __repr__(self):
#         return "<CEFR {}>".format(self.cefr)
#
# class POS(Base):
#     __tablename__ = 'pos'
#
#     id = Column(Integer(), primary_key=True)
#     definition_id = Column(Integer, ForeignKey('definition.id'))
#     pos = Column(String(50))
#
#     def __repr__(self):
#         return "<CEFR {}>".format(self.cefr)
#
# class Example(Base):
#     __tablename__ = 'example'
#
#     id = Column(Integer(), primary_key=True)
#     definition_id = Column(Integer, ForeignKey('definition.id'))
#     example = Column(String(4096))
#
#     def __repr__(self):
#         return "<Example {}>".format(self.example)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///vocab-model')
drop_database(engine.url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()


for word in word_list[:25]:
    wm = datamodel.Word(word)
    w = Word(word=word, cefr=wm.cefr)
    for sense in wm:
        definition = Sense(definition= sense.definition, word=w)
    s.add(w)
    s.commit()

# for item in s.query(Word).filter(Word.word=='burial'):
#     print(item.senses[0])
