from collections import Counter

from django.db.models import F
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404

from quiz.classes.slide import create_slide, get_slide
from quiz.constants import QuestionClass, QuestionType, RoundType
from quiz.models import (Category, Choice, ChoiceAnswer, NormalAnswer, OrderAnswer,
                         Question, QuestionScores, QuestionSlide, Round, Score)


class BaseQuestion:
    editable_fields = ['type', 'description', 'points', 'degradation', 'multiplier', 'category_id']

    def __init__(self, question):
        self.question = question
        
        self.slide_qs = QuestionSlide.objects.filter(question=self.question)
        self.slides = [
            get_slide(qs.slide) for qs in self.slide_qs
        ]
    
    def host_info(self):
        info = model_to_dict(self.question)
        return {
            **info,
            'class': self.question_class,
            'slides': [{
                **model_to_dict(qs),
                'slide': slide.info(),
            } for qs, slide in zip(self.slide_qs, self.slides)],
            'answer': self.answer_info(),
        }
    
    def player_info(self):
        return model_to_dict(self.question)

    def answer_info(self):
        pass

    def award_points(self, user, points):
        QuestionScores.objects.create(user=user, question=self.question, score=points)

        quiz_score = Score.objects.get_or_create(quiz=self.question.round.quiz, user=user)
        quiz_score.score += F('score') + points
        quiz_score.save()
    
    @staticmethod
    def create(question_info):
        return Question.objects.create(**question_info)

    def edit(self, question_info):
        if 'type' in question_info and question_info['type'] != self.question.type:
            self.delete_answers()
        self.question.__dict__.update(question_info)
        self.question.save()

    def delete_answers(self):
        pass

    def get_slide_or_404(self, slide_id):
        return get_object_or_404(self.slide_qs, pk=slide_id)

    def create_slide(self, slide_info):
        slide = create_slide(slide_info)
        slide_number = self.slide_qs.count() + 1
        QuestionSlide.objects.create(
            question=self.question,
            slide=slide,
            slide_number=slide_number
        )

    def edit_slide(self, slide_id, slide_info):
        slide = self.get_slide_or_404(slide_id).slide
        get_slide(slide).edit(slide_info)

    def delete_slide(self, slide_id):
        slide = self.get_slide_or_404(slide_id)
        self.slide_qs.filter(slide_number__gt = slide.slide_number).update(slide_number=F('slide_number') - 1)
        get_slide(slide.slide).delete()

    def delete_slides(self):
        for slide in self.slides:
            slide.delete()

    def delete(self):
        self.delete_answers()
        self.delete_slides()
        self.question.delete()

    def get_next_slide_number(question_id):
        rounds = Round.objects.filter(quiz_id=quiz_id)
        if rounds.exists():
            greatest_round = rounds.aggregate(Max('round_number'))
            return greatest_round['round_number__max'] + 1
        return 1

class NormalQuestion(BaseQuestion):
    question_class = QuestionClass.SINGLE_ANSWER

    def __init__(self, question):
        assert question.type == QuestionType.NORMAL

        super().__init__(question)

        self.answer = NormalAnswer.objects.filter(question=self.question)
        if self.answer.exists():
            self.answer_slide = get_slide(self.answer[0].slide)

    def answer_info(self):
        if self.answer.exists():
            return {
                **model_to_dict(self.answer[0]),
                'slide': self.answer_slide.info()
            }
        else:
            return None

    def award_points(self, user):
        question_score = self.question.points * self.question.multiplier
        super().award_points(user, question_score)

    def set_answer(self, answer_info):
        if self.answer.exists():
            # TODO: Return exception
            pass
        answer_slide = create_slide(answer_info)
        answer = NormalAnswer.objects.create(
            question=self.question,
            slide=answer_slide
        )

    def edit_answer(self, answer_info):
        if self.answer.exists():
            info = answer_info.get('info', '')
            self.answer_slide.edit(info)
        else:
            # TODO: Return exception
            pass

    def delete_answer(self):
        if self.answer.exists():
            self.answer_slide.delete()
        else:
            # TODO: Return exception
            pass

    def delete_answers(self):
        if self.answer.exists():
            self.answer_slide.delete()
        # No exception here waav

class ChoiceQuestion(BaseQuestion):
    question_class = QuestionClass.CHOICE_ANSWER

    def __init__(self, question):
        super().__init__(question)

        self.choices = Choice.objects.filter(question=self.question)
        self.choice_slides = [get_slide(choice.slide) for choice in self.choices]

    def host_info(self):
        info = super().host_info()
        info['choices'] = [
            {
                **model_to_dict(choice),
                'slide': slide.info(),
            } for choice, slide in zip(self.choices, self.choice_slides)
        ]
        return info

    def player_info(self):
        info = super().player_info()
        info['choices'] = len(self.choice_slides)
        return info

    def get_choice_or_404(self, choice_id):
        return get_object_or_404(self.choices, pk=choice_id)

    def add_choice(self, choice_info):
        choice_slide = create_slide(choice_info)
        choice_number = self.choices.count() + 1
        Choice.objects.create(
            question=self.question,
            slide=choice_slide,
            choice_number = choice_number
        )

    def edit_choice(self, choice_id, choice_info):
        info = choice_info.get('info', '')
        get_slide(self.get_choice_or_404(choice_id).slide).edit(info)

    def delete_choice(self, choice_id):
        choice = self.get_choice_or_404(choice_id)
        self.choices.filter(choice_number__gt=choice.choice_number).update(choice_number=F('choice_number') - 1)
        get_slide(choice.slide).delete()

    def delete_choices(self):
        for slide in self.choice_slides:
            slide.delete()
    
    def delete_answers(self):
        self.delete_choices()

class MCQuestion(ChoiceQuestion):
    def __init__(self, question):
        assert question.type == QuestionType.MCQ
        super().__init__(question)

        self.choice_answer = ChoiceAnswer.objects.filter(question=self.question)
        if self.choice_answer.exists():
            self.answer = self.choice_answer[0].choice.choice_number

    def answer_info(self):
        if self.choice_answer.exists():
            return self.answer
        else:
            return None

    def award_points(self, user, answer):
        question_points = self.question.points * self.question.multiplier
        
        num_answered = QuestionScores.objects.filter(question=question).count()

        if answer == self.answer:
            degradation = self.question.degradation ** num_answered
        else:
            degradation = - ((1 - self.question.degradation) ** num_answered)

        question_points = question_points * degradation
        super().award_points(user, question_points)

    def set_answer(self, answer_info):
        try:
            choice_id = answer_info.get('choice_id')
        except e:
            # TODO: Return exception
            pass

        choice = self.get_choice_or_404(choice_id)
        ChoiceAnswer.objects.update_or_create(
            question=self.question, 
            defaults={'choice': choice}
        )

class OrderQuestion(ChoiceQuestion):
    def __init__(self, question):
        assert question.type == QuestionType.ORDERING
        super().__init__(question)

        self.choices = Choice.objects.filter(question=self.question)
        self.choice_slides = [get_slide(choice.slide) for choice in self.choices]

        self.order_answer = OrderAnswer.objects.filter(question=self.question)
        if self.order_answer.exists():
            self.answer = [int(x) for x in self.order_answer[0].order.split(',')]

    def answer_info(self):
        if self.order_answer.exists():
            return self.answer
        else:
            return None
    
    def award_points(self, user, answer):
        question_points = self.question.points * self.question.multiplier
        
        num_answered = QuestionScores.objects.filter(question=question).count()

        if answer == self.answer:
            degradation = self.question.degradation ** num_answered
        else:
            degradation = - ((1 - self.question.degradation) ** num_answered)

        question_points = question_points * degradation
        super().award_points(user, question_points)

    def delete_choice(self, choice_id):
        super().delete_choice(choice_id)
        self.order_answer.delete()

    def add_choice(self, choice_info):
        super().add_choice(choice_info)
        self.order_answer.delete()

    def set_answer(self, answer_info):
        try:
            order = answer_info.get('order')
        except e:
            # TODO: Return exception
            pass

        counts = Counter([int(x) for x in order.split(',')])
        for i in range(len(self.choices)):
            if counts[i+1] != 1:
                # TODO: Exception, invalid order
                return
        OrderAnswer.objects.update_or_create(
            question=self.question,
            defaults={'order': order}
        )

    def delete_answers(self):
        if self.order_answer.exists():
            OrderAnswer.objects.get(question=self.question).delete()
        
        super().delete_answers()

questions = {
    QuestionType.NORMAL: NormalQuestion,
    QuestionType.MCQ: MCQuestion,
    QuestionType.ORDERING: OrderQuestion,
}

def get_question(question):
    return questions[question.type](question)

def create_question(question_info):
    return questions[question_info['type']].create(question_info)

def edit_question(question, question_info):
    questions[question.type](question).edit(question_info)

def delete_question(question):
    questions[question.type](question).delete()

def filter_question_info(question_info):
    if 'type' not in question_info or question_info['type'] not in QuestionType.values:
        question_info['type'] = QuestionType.NORMAL

    return { key:value for key, value in question_info.items() if key in BaseQuestion.editable_fields }

def create_question_or_404(user, quiz_id, round_id, question_info):
    round = get_object_or_404(Round, pk=round_id, quiz_id=quiz_id, quiz__host=user)

    question_info['round_id'] = round.id
    
    if round.type == RoundType.BOARD:
        if 'category_id' not in question_info:
            # TODO: Bad request response
            pass
        if not Category.objects.filter(pk=question_info['category_id'], round_id=round_id).exists():
            # TODO: Bad request response
            pass

    if round.type == RoundType.SEQUENTIAL:
        last_question = Question.objects.filter(round=round).order_by('question_number').last()
        if last_question == None:
            question_info['question_number'] = 1
        else:
            question_info['question_number'] = last_question.question_number + 1
    
    return create_question(question_info)

def get_question_or_404(user, quiz_id, round_id, question_id):
    question = get_object_or_404(Question, pk=question_id, round_id=round_id, round__quiz_id=quiz_id, round__quiz__host=user)
    return get_question(question)