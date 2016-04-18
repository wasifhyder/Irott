# import random
import click
# from quiz import Question
# from student.test_student_model import Student
# from domain.word_lists import word_list
# from instructor.quiz import generate_definition_question
from engine.domain.filemodel import DomainModel
from engine.student.jsonmodel import StudentModel
from engine.instructor.instructor import Instructor

@click.command()
def hello():
    click.echo("Hello. How are you?")

if __name__ == "__main__":
    # username, password = tuple(input("Hello. Welcome to the Vocabulary ITS\n"
          # "To begin enter your username and password: ").split())
    username = "wasif"
    password = "123"

    s = StudentModel(username, password)
    d = DomainModel()
    I = Instructor(d, s, 3)

    choice = 1
    while True:
        print("\n"
              "[0] Check Vocabulary Profile\n"
              "[1] Take a Quiz (3 questions)\n"
              "[2] Quit")
        choice = int(input())
        if choice == 0:
            while True:
                choice = input("Enter a word to search, or 'b' to go back, or 'x' to quit: ").lower()
                if choice == 'x':
                    break
                if choice == 'b':
                    break
                else:
                    print("You asked for {}".format(choice))
                    try:
                        print(s[choice])
                    except KeyError:
                        print("Word not found. Try another one.")
            if choice == 'x': break
        elif choice == 1:
            I.quiz()
        elif choice == 2:
            break

    pass
