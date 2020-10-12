from django.forms import model_to_dict
from django.shortcuts import get_object_or_404

from quiz.models import Quiz as QuizModel, Round, QuizState
from quiz.classes.round import get_round

class Quiz:
    editable_fields = ['name', 'secret']

    def __init__(self, quiz):
        self.quiz = quiz
        self.state, _ = QuizState.objects.get_or_create(quiz=self.quiz)
        self.round_qs = Round.objects.filter(quiz=self.quiz)
        self.rounds = [get_round(r) for r in self.round_qs]

    def edit_info(self):
        return {
            **model_to_dict(self.quiz),
            'started': self.state.started,
            'ended': self.state.ended,
            'rounds': [r.base_info() for r in self.rounds]
        }

    def info(self):
        return {
            'name': self.quiz.name,
            'host': self.quiz.host.username,
            'rounds': [r.base_info() for r in self.rounds]
        }

    @staticmethod
    def create(quiz_info):
        return QuizModel.objects.create(**quiz_info)

    def edit(self, quiz_info):
        self.quiz.__dict__.update(quiz_info)
        self.quiz.save()

    def delete(self):
        [r.delete() for r in self.rounds]
        self.quiz.delete()

    def next_round(self):
        if self.state.round == None:
            self.state.round_id = self.round_qs[0].id
        elif self.state.round.round_number == self.round_qs.count():
            # TODO: Raise Exception
            return None
        else:
            self.state.round_id = self.round_qs[self.state.round.round_number].id

        self.state.save()

def create_quiz(user, quiz_info = {}):
    quiz_info = filter_quiz_info(quiz_info)

    quiz_info['host_id'] = user.id

    return Quiz.create(quiz_info)

def get_quiz(quiz):
    return Quiz(quiz)

def get_quiz_or_404(user, quiz_id):
    quiz = get_object_or_404(QuizModel, pk=quiz_id, host_id=user.id)
    return Quiz(quiz)

def filter_quiz_info(quiz_info):
    return { key:value for key, value in quiz_info.items() if key in Quiz.editable_fields }