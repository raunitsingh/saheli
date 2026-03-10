from .symptom_protocol import SYMPTOM_PROTOCOL


class InterviewEngine:

    def __init__(self):
        self.current_symptom = None
        self.question_index = 0
        self.answers = []
        self.questions = []

    def start_interview(self, symptom):

        if symptom not in SYMPTOM_PROTOCOL:
            return None

        self.current_symptom = symptom
        self.question_index = 0
        self.answers = []

        self.questions = SYMPTOM_PROTOCOL[symptom]["questions"]

        return self.questions[0]

    def next_question(self, answer):

        self.answers.append(answer)

        self.question_index += 1

        if self.question_index < len(self.questions):
            return self.questions[self.question_index]

        return None

    def get_results(self):

        result = {}

        for i, question in enumerate(self.questions):
            if i < len(self.answers):
                result[question] = self.answers[i]

        return result