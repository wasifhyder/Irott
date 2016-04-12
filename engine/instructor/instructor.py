import random
from nltk.corpus import wordnet as wn
# from domain.word_lists import load_word_list
from domain.word_frequency import similar_freq_words
# from domain.datamodel import Word

from student.filemodel import StudentModel
from domain.filemodel import DomainModel

"""
The best way to design would be to talk things out. Right now, I'm trying to
create a quizzing engine. The quizzing engine supports the asking

"""
class QuizEngine:
    pass

class Instructor:
    """
        Quiz can have three types of quizzes at the very least:
            > Assessment: Figures out which words are trouble / known
            > Review: Any question we get as wrong is used as a review question
            > Progress: Repeatedly questions until the word is mastered
        There are a few ways in which I can handle the questions. An important way of looking
        into this is to determine based on the mastery level what type of question.
            > 0      : Word hasn't been introduced yet.  Assessment
            > 1-60   : Word is in review. The first correct answer puts you in this range.
            > 60-90  : Word is close to being mastered
            > 90-100 : Word can be considered mastered
    """
    def __init__(self, domain_model, student_model, n=10):
        # Generate 10 questions using the domain model
        # Ask each question
        # Update the student model based on the answer to each question
        # Update the quiz history of the student
        self.domain_model = domain_model
        self.student_model = student_model
        self.n = n
        # Ask 10 questions
        # Create a question automatically
        # If question answered correctly - Improve score
        # If question answered incorrectly - Reduce score
        # The improvement or reduction of score should atleast be dependent on the
        # spaced repetition system. Improvement reduction of score should also be
        # dependent based on Item Response Theory

        pass

    def quiz(self):
        i = 0
        words = self.student_model.words()
        for word in random.sample(words, self.n):
            q = self.generate_definition_question(word)
            sense = q.sense.name
            correct = q.ask()
            print(word)
            print(sense)
            self.student_model[word][sense].update(correct)
        self.student_model.save()

    def get_quiz(self):
        words = self.student_model.words()
        word = random.choice(words)
        q = self.generate_definition_question(word)
        sense = q.sense.name

        result = {
            'word': word,
            'sense': sense,
            'prompt': q.prompt,
            'correct': q.correct,
            'incorrect': q.incorrect,
            'feedback': q.feedback
        }
        print(result['incorrect'])
        return result

    # def update_quiz(self, correct):

    def generate_question(self):
        # Use the automatic question generation technique
        # Some automatically generated questions can automatically be stored
        # This may be useful in content management later
        type = random.choice("definition", "synonym", "antonym")
        if type == "definition":
            self.generate_definition_question()
        elif type == "synonym":
            pass
        elif type == "antonym":
            pass
        pass

    def generate_definition_question(self, word, prompt="What's the meaning of the word {}"):
        """
            Method: Find the definitions of the word. Choose the definition that doesn't include the target
                    word
        """
        # Filters out the definition the contains the target word
        # Todo: Expand the filter to exclude morphological forms
        senses = self.domain_model[word]
        candidates = [sense for sense in senses if word not in sense.definition]
        sense = random.choice(candidates)
        # Generate Question
        # First randomly select a definition
        definition = sense.definition
        pos = sense.pos
        try:
            # Get words in the same part of speech that have similar frequency
            # First returns a list of similar frequency words
            # Then chooses 3 candidates

            distractor_candidates = random.sample(similar_freq_words(word, pos), 3)
            # For each distractor, find the definition
            # Make sure the part of speech matches
            distractors = []
            for candidate in distractor_candidates:
                distractor = random.choice([sense.definition for sense in
                                            self.domain_model[candidate] if sense.pos == pos])
                distractors.append(distractor)
        except (KeyError, IndexError) as e:
            print("Couldn't find the frequency for this word")
            print(e)

        return Question(sense, prompt, correct=definition, incorrect=distractors)


class Question:
    def __init__(self, sense, prompt, correct, incorrect, feedback=""):
        self.sense = sense
        self.word = "".join(sense.name.split('.')[0:-2])
        self.prompt = prompt
        self.correct = correct
        self.incorrect = incorrect
        self.feedback = feedback

    def ask(self):
        # Ask the question
        print(self.prompt.format(self.word))
        choices = self.incorrect + [self.correct]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            print("[{}]: {}".format(i, choice))

        answer = int(input())
        if choices[answer] == self.correct:
            print("That is correct")
            return True
        else:
            if self.feedback == "":
                self.feedback = "The correct answer is {}".format(self.correct)

            print("Incorrect\n"
                  "{}".format(self.feedback))
            return False



if __name__ == "__main__":
    s = StudentModel('wasif', '123')
    d = DomainModel()
    print(s.wordsSeen())
    q = Instructor(d, s, 20)
    q.quiz()

    print(s.wordsSeen())
    # word_list = load_word_list()
    # for word in random.sample(word_list, 10):
    #     try:
    #         generate_definition_question(word).ask()
    #     except Exception:
    #         print("Couldn't generate question for the word {}".format(word))


