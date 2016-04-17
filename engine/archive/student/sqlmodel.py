from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Boolean, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SenseQuestions = Table('sense_questions', Base.metadata,
                       Column('sense_profile', Integer, ForeignKey('sense_profile.id')),
                       Column('question', Integer, ForeignKey('question.id'))
                       )

class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True)
    # belongs-to-one Question
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="choices", uselist=False)

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    # belongs-to-many senses
    sense_profile = relationship("SenseProfile", secondary=SenseQuestions, back_populates="questions")
    prompt = Column(String(4096))
    # has-many choices
    choices = relationship("Choice", back_populates="question")
    # Other fields
    correct_choice = Column(String(4096), nullable=False)
    is_correct = Column(String(4096), nullable=False)
    date_asked = Column(Date, nullable=False)

class SenseProfile(Base):
    __tablename__ = 'sense_profile'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("word_profile.id"))
    questions = relationship("Question", secondary=SenseQuestions, back_populates="sense_profile")
    sense_score_history = relationship("SenseScoreHistory", back_populates="sense_profile")

    word_profile = relationship("WordProfile", back_populates="sense_profile", uselist=False)
    name = Column(String(60), nullable=False)
    score = Column(Float, default=0.0)

    def __repr__(self):
        return "<{}:{}>".format(self.name, self.score)


class SenseScoreHistory(Base):
    __tablename__ = 'sense_score_history'
    id = Column(Integer, primary_key=True)
    sense_profile_id = Column(Integer, ForeignKey("sense_profile.id"))
    sense_profile = relationship("SenseProfile", back_populates="sense_score_history", uselist=False)


class WordProfile(Base):
    __tablename__ = 'word_profile'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))

    sense_profile = relationship("SenseProfile", back_populates="word_profile")
    word_score_history = relationship("WordScoreHistory", back_populates="word_profile")

    student = relationship("Student", back_populates="word_profile")
    word = Column(String(50), nullable=False)
    cefr = Column(String(3), nullable=False)
    score = Column(Float, default=0.0)
    active = Column(Boolean, default=False)
    activation_date = Column(Date)

class WordScoreHistory(Base):
    __tablename__ = 'word_score_history'
    id = Column(Integer, primary_key=True)
    word_profile_id = Column(Integer, ForeignKey("word_profile.id"))
    word_profile = relationship("WordProfile", back_populates="word_score_history", uselist=False)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(Integer, nullable=False)
    word_profile = relationship("WordProfile", uselist=False, back_populates="student")


from engine.domain.filemodel import DomainModel
if __name__ == "__main__":
    engine = create_engine("mysql+pymysql://root@localhost/irott?host=localhost?port=3306")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    d = DomainModel()

    student = Student(username="empty", password="")

    wps = []
    for w in sorted(d.word_list.keys()):
        word = d[w].word
        cefr = d[w].cefr
        wp = WordProfile(student=student, word=word, cefr=cefr)
        for s in d[w]:
            name = s.name
            found = session.query(SenseProfile).filter(SenseProfile.name == name).all()
            SenseProfile(word_profile=wp, name=name)
        wps.append(wp)
    session.add_all(wps)
    session.add(student)
    session.commit()