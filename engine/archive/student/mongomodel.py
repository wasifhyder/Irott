import json
from bson import json_util

from mongoengine import EmbeddedDocument, StringField, DateTimeField, FloatField, \
    ListField, IntField, EmbeddedDocumentField, Document, connect, \
    ReferenceField


from engine.domain.filemodel import DomainModel


class Quiz(EmbeddedDocument):
    prompt = StringField()
    question = StringField()
    choices = StringField()
    correct = StringField()
    answer_correct = StringField(required=True, choices=['True','False'])
    date_asked = DateTimeField(required=True)


class SenseProfile(Document):
    parent = StringField(required=True)
    name = StringField(required=True)
    score = FloatField(required=True, default=0.0)
    accuracy_model = ListField(IntField(required=True, choices=[0,1]), required=True, default=
                               [0 for x in range(20)])
    quiz_history = ListField(EmbeddedDocumentField(Quiz), default=[])

class WordProfile(EmbeddedDocument):

    word = StringField(required=True)
    cefr = StringField(required=True, choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'U0'])
    score = FloatField(required=True, default=0.0)
    sense_profile = ListField(ReferenceField(SenseProfile))

    meta = {'indexes': [
                'word',
                'score',
                'cefr',
                'sense_profile.name',
                'sense_profile.score',
            ],
            'ordering': '+vocabulary_profile.score'
            }

    def __repr__(self):
        return "Hello Ma"

class StudentModel(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    vocabulary_profile = ListField(EmbeddedDocumentField(WordProfile))

    meta = {'collection': 'student',
            'indexes': [
                'username',
                'vocabulary_profile.word',
                'vocabulary_profile.score',
                'vocabulary_profile.cefr'
            ],
    }


seen = {}
def create_student_model():
    student = StudentModel()
    student.username = "wasif"
    student.password = "123"
    student.vocabulary_profile = []
    d = DomainModel()
    for word in d:
        wp = WordProfile()
        wp.word = word
        wp.score = 0
        wp.cefr = d[word].cefr
        wp.sense_profile = []
        for sense in d[word]:
            sp = SenseProfile()
            sp.parent = word
            sp.name = sense.name
            sp.score = 0
            sp.accuracy_model = [0 for x in range(20)]
            sp.quiz_history = []
            wp.sense_profile.append(sp)
        student.vocabulary_profile.append(wp)
    student.save()


if __name__ == "__main__":
    connect('irott')


    student = StudentModel.objects(username="wasif")[0]
    vocabulary_profile = student.vocabulary_profile

    pass



