from collections import defaultdict

from django.db.models import F, Max
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404

from quiz.classes.question import delete_question
from quiz.constants import RoundType
from quiz.models import Category, Question, Quiz, Round


class BaseRound:

    editable_fields = ['name', 'degradation']

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

    def edit(self, round_info):
        self.round.__dict__.update(round_info)
        self.round.save()
        # return Round.objects.filter(pk=round_id).update(**round_info)

    def delete(self):
        Round.objects.filter(
            quiz_id=self.round.quiz_id, 
            round_number__gt=self.round.round_number
        ).update(
            round_number=F('round_number') - 1
        )

        self.round.delete()

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

        self.categories = Category.objects.filter(round_id=self.round.id)

    def info(self):
        info = super().info()
        
        questions = defaultdict(list)
        for q in self.questions.order_by('points'):
            questions[q.category_id].append(model_to_dict(q))

        info['categories'] = [
            {
                **model_to_dict(category),
                'questions': questions[category.id]
            } for category in self.categories
        ]

        return info
    
    def edit_info(self):
        return self.info()

    def get_category_or_404(self, category_id):
        return get_object_or_404(self.categories, pk=category_id)

    def add_category(self, name):
        Category.objects.create(round_id=self.round.id, name=name)

    def rename_category(self, category_id, name):
        category = self.get_category_or_404(category_id)
        category.name = name
        category.save()

    def delete_category(self, category_id):
        self.get_category_or_404(category_id).delete()     

    def delete(self):
        self.categories.delete()
        super().delete()    

rounds = {
    RoundType.SEQUENTIAL: SequentialRound,
    RoundType.BOARD: BoardRound
}

def get_round(round):
    return rounds[round.type](round)

def get_round_or_404(user, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id, quiz_id=quiz_id, quiz__host_id=user.id)
    return get_round(round)

def get_category_round_or_404(user, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id, type=RoundType.BOARD, quiz_id=quiz_id, quiz__host_id=user.id)
    return BoardRound(round)

def create_round_or_404(user, quiz_id, round_info={}):
    quiz = get_object_or_404(Quiz, pk=quiz_id, host_id=user.id)

    round_info['quiz_id'] = quiz_id

    round_info['round_number'] = Round.objects.filter(quiz_id=quiz_id).count() + 1

    if 'type' not in round_info or round_info['type'] not in RoundType.values:
        round_info['type'] = RoundType.SEQUENTIAL

    return rounds[round_info['type']].create(round_info)

def edit_round(round_id, round_info):
    return rounds[round_info.type].edit(round_id, round_info)

def delete_round(round):
    rounds[round.type](round).delete()

def filter_round_info(round_info):
    if 'degradation' in round_info:
        round_info['degradation'] = min(1, max(0, float(round_info['degradation'])))
    return { key:value for key, value in round_info.items() if key in BaseRound.editable_fields }
