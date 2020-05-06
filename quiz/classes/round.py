from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.db.models import Max

from django.forms import model_to_dict

from quiz.models import Round, Question
from quiz.classes.question import delete_question
from quiz.constants import RoundType

class BaseRound:

    editable_fields = ['name']

    def __init__(self, round):
        self.round = round
        self.questions = Question.objects.filter(round=self.round)

    def info(self):
        return model_to_dict(self.round)

    def base_info(self):
        return model_to_dict(self.round)

    @staticmethod
    def create(round_info):
        return Round.objects.create(**round_info)

    @staticmethod
    def edit(round_id, round_info):
        return Round.objects.filter(pk=round_id).update(**round_info)

    def delete(self):
        [delete_question(q) for q in self.questions]
        self.round.delete()
    
    @staticmethod
    def get_greatest_round(quiz):
        if Round.objects.filter(quiz=quiz).exists():
            greatest_round = Round.objects.filter(quiz=quiz).aggregate(Max('round_number'))
            return greatest_round['round_number__max'] + 1
        return 1

class SequentialRound(BaseRound):
    def __init__(self, round):
        assert round.type == RoundType.SEQUENTIAL
        super().__init__(round)

    def info(self):
        info = super().info()
        info['questions'] = [model_to_dict(q) for q in self.questions]
        return info
    
    def edit_info(self):
        round = super().base_info()
        round['type'] = 'SEQUENTIAL'
        return {
           **round,
           'questions':  [model_to_dict(q) for q in self.questions]
        }

    # TODO depending on how sockets work
    def next_question(self):
        pass
    
class BoardRound(BaseRound):
    def __init__(self, round):
        assert round.type == RoundType.BOARD
        super().__init__(round)

    def info(self):
        info = super().info()
        
        questions = defaultdict(list)
        for q in self.questions.order_by('points'):
            questions[q.category].append(model_to_dict(q))
        info['questions'] = questions

        return info
    
    def edit_info(self):
        info = self.info()
        info['type'] = 'BOARD'
        return {
           **info 
        }

rounds = {
    RoundType.SEQUENTIAL: SequentialRound,
    RoundType.BOARD: BoardRound
}

def get_round(round):
    return rounds[round.type](round)

def get_round_or_404(quiz, round_id):
    round = get_object_or_404(Round, pk=round_id, quiz=quiz)
    return rounds[round.type](round)

def create_round(quiz, round_info = {}):
    round_info['quiz'] = quiz.quiz
    round_info['round_number'] = rounds[round_info['type']].get_greatest_round(quiz.quiz)
    return rounds[round_info['type']].create(round_info)

def edit_round(round_id, round_info):
    return rounds[round_info.type].edit(round_id, round_info)

def delete_round(round):
    rounds[round.type](round).delete()

def filter_round_info(round_info):
    return { key:value for key, value in round_info.items() if key in BaseRound.editable_fields }