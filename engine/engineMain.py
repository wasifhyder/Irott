# import random
import click
# from quiz import Question
# from student.test_student_model import Student
# from domain.word_lists import word_list
# from instructor.quiz import generate_definition_question


@click.command()
def hello():
    click.echo("Hello. How are you?")

if __name__ == "__main__":
    hello()
    # print("Hello. Welcome to the Vocabulary ITS\n"
    #       "To begin enter your username and password: ")
    # username, password = tuple(input().split())
    # username = "Wasif"
    # password = "pass"

    # s = Student(username, password)




    # choice = 1
    # while True:
    #     print("\n"
    #           "[0] Check Vocabulary Profile\n"
    #           "[1] Take a Quiz")
    #     # choice = int(input())
    #     if choice == 0:
    #         while True:
    #             choice = input("Enter a word to search, or 'x' to quit: ").lower()
    #             if choice == 'x':
    #                 break
    #             else:
    #                 print("You asked for {}".format(choice))
    #                 try:
    #                     print(s.get_word_profile(choice))
    #                 except KeyError:
    #                     print("Word not found. Try another one.")
    #         break
    #     elif choice == 1:
    #         for word in random.sample(word_list, 3):
    #             q = generate_definition_question(word)
    #             s.update_score(q.sense, q.ask())
    #         choice = 0
    #
    # pass
