from flask import Flask, render_template

app = Flask(__name__)


from flask import Flask, jsonify
from flask import render_template
from flask.ext.bootstrap import Bootstrap

from ..engine.domain.filemodel import DomainModel
from ..engine.student.filemodel import StudentModel
from ..engine.instructor.instructor import Instructor

app = Flask(__name__)
Bootstrap(app)

S = StudentModel('wasif', '123')
D = DomainModel()


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/word/<word>')
def word(word):
    return jsonify(D[word].json())


@app.route('/quiz/', methods=['GET'])
def quiz():
    I = Instructor(D, S, 20)
    return jsonify(I.get_quiz())

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=81)