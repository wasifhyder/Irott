from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()

# WordDefinition = Table('word_definitions',
#                        Base.metadata,
#                        Column('word_id', String, ForeignKey('words.id'), primary_key=True),
#                        Column('definition_id', String, ForeignKey('definitions.id'), primary_key=True))

class Word(Base):
    """
    A word can have:
        Definitions: 1 or more
    """
    __tablename__ = 'word'
    id = Column(Integer(), primary_key=True)
    word = Column(String(50), unique=True)

    definitions = relationship("Definition", backref="word")

    def __repr__(self):
        return "<Word {}>".format(self.word)


class Definition(Base):
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
    __tablename__ = 'definition'

    id = Column(Integer(), primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id'))
    definition = Column(String(50))

    examples = relationship("Example", backref="definition")
    synonyms = relationship("Synonym", backref="definition")

    cefr = relationship("CEFR", backref=backref("definition", uselist=False))
    pos = relationship("POS", backref=backref("definition", uselist=False))

    def __repr__(self):
        return "<Definition {}>".format(self.definition)

class CEFR(Base):
    __tablename__ = 'cefr'

    id = Column(Integer(), primary_key=True)
    definition_id = Column(Integer, ForeignKey('definition.id'))
    cefr = Column(String(12))

    def __repr__(self):
        return "<CEFR {}>".format(self.cefr)

class POS(Base):
    __tablename__ = 'pos'

    id = Column(Integer(), primary_key=True)
    definition_id = Column(Integer, ForeignKey('definition.id'))
    pos = Column(String(50))

    def __repr__(self):
        return "<CEFR {}>".format(self.cefr)

class Example(Base):
    __tablename__ = 'example'

    id = Column(Integer(), primary_key=True)
    definition_id = Column(Integer, ForeignKey('definition.id'))
    example = Column(String(4096))

    def __repr__(self):
        return "<Example {}>".format(self.example)




from sqlalchemy import create_engine
engine = create_engine('sqlite:///vocab-model')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()

# Code - Example of adding a word
# If word already exists in database, the definition will have to be added to
# word1 = Word(word="Between")
# definition1 = Definition(definition="Exists among two", word=word1)
# cefr1 = CEFR(cefr="A1", definition=definition1)
# # definition1.cefr = cefr1
# example1 = Example(example="Between us we fight", definition=definition1)
# example12 = Example(example="There's nothing between us any more", definition=definition1)
# s.add(word1)
# s.commit()
# print(s.query(Word).all())
# print(s.query(Definition).all())

# Query that shows the words
# SELECT word, definition, cefr
# FROM word JOIN definition INNER JOIN cefr
# WHERE word.id = definition.word_id AND definition.id = cefr.definition_id
