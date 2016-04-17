# from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Boolean, Date
# from sqlalchemy import create_engine
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# from engine.domain.word_frequency import get_word_frequency_all, get_word_frequency
#
# Base = declarative_base()
#
# WordSense = Table('wordsense', Base.metadata,
#     Column('word_id', Integer, ForeignKey('word.id')),
#     Column('sense_id', Integer, ForeignKey('sense.id'))
# )
#
# WordSynonyms = Table('wordsynonyms', Base.metadata,
#     Column('word_id', Integer, ForeignKey('word.id')),
#     Column('sense_id', Integer, ForeignKey('sense.id'))
# )
#
# WordAntonyms = Table('wordantonyms', Base.metadata,
#     Column('word_id', Integer, ForeignKey('word.id')),
#     Column('sense_id', Integer, ForeignKey('sense.id'))
# )
#
# class Frequency(Base):
#     __tablename__ = 'frequency'
#     id = Column(Integer, primary_key=True)
#     sense_id = Column(Integer, ForeignKey("sense.id"))
#     sense = relationship("Word", uselist=False, back_populates="frequency")
#     total = Column(Integer, required=True)
#     n = Column(Integer, default=0)
#     v = Column(Integer, default=0)
#     a = Column(Integer, default=0)
#
#
# class Word(Base):
#     __tablename__ = 'word'
#     id = Column(Integer, primary_key=True)
#     word = Column(String(50))
#     cefr = Column(String(50))
#     frequency = relationship("Frequency", uselist=False, back_populates="sense")
#     senses = relationship("Sense", secondary=WordSense, back_populates="words")
#     sense_synonyms = relationship("Sense", secondary=WordSynonyms, back_populates="synonyms")
#     sense_antonyms = relationship("Sense", secondary=WordAntonyms, back_populates="antonyms")
#
#
# class Sense(Base):
#     __tablename__ = 'sense'
#     id = Column(Integer, primary_key=True)
#     words = relationship("Word", secondary=WordSense, back_populates="senses")
#     name = Column(String(60), unique=True)
#     pos = Column(String(3), nullable=False)
#     definition = Column(String(4096), nullable=False)
#     examples = relationship("Example", back_populates="sense")
#     synonyms = relationship("Word", secondary=WordSynonyms, back_populates="sense_synonyms")
#     antonyms = relationship("Word", secondary=WordAntonyms, back_populates="sense_antonyms")
#
# class Example(Base):
#     __tablename__ = 'example'
#     sense_id = Column(Integer, ForeignKey("sense.id"))
#     # These values are to be entered
#     sense = relationship("Sense", uselist=False, back_populates="examples")
#     example = Column(String(4096), nullable=False)
#
# words = {}
# def create_word(w):
#     if w in words:
#         return words[w]
#     else:
#         word = d[w].word
#         cefr = d[w].cefr
#         # Frequency
#         mword_frequencies = get_word_frequency_all(word)
#         a, n, v, total = 0, 0, 0, get_word_frequency(word)
#         for pos in ['a', 'n', 'v']:
#             if mword_frequencies != 0 and pos in mword_frequencies:
#                 if pos == 'a': a = mword_frequencies[pos]
#                 if pos == 'n': n = mword_frequencies[pos]
#                 if pos == 'v': v = mword_frequencies[pos]
#
#         sFrequency = Frequency(total=total, a=a, n=n, v=v)
#         sWord = Word(word=word, cefr=cefr, frequency=sFrequency)
#         senses = []
#         for s in d[w]:
#             name = s.name
#             pos = s.pos
#             definition = s.definition
#             sSense = Sense(name=name, pos=pos, definition=definition, word=word)
#             examples = [Example(sense=sSense, example=example) for example in s.examples]
#             synonyms = []
#             for synonym in s.synonyms:
#                 if word in words:
#
#             examples = [Example(sense=sense, example=example) for example in s.examples]
#
#             senses.append(sense)
#
# from engine.domain.filemodel import DomainModel
# if __name__ == "__main__":
#     engine = create_engine("mysql+pymysql://root@localhost/irott?host=localhost?port=3306")
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     d = DomainModel()
#
#
#
#
#     session.add_all(words.values())
#     session.commit()