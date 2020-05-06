from django.views import View
from django.shortcuts import render, redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.round import create_round, get_round_or_404, filter_round_info
from quiz.classes.quiz import get_quiz_or_404
from quiz.classes.quiz import get_quiz_or_404
from quiz.constants import QuestionType

class CreateRoundView(LoginRequiredMixin, View):
    
    def post(self, request, quiz_id):
        '''
        Create a round
        Attributes:
            body containing round_info
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)
        round_info = {
            'type': request.POST.get('round_type')
        }
        round = create_round(quiz_wrapper, round_info)
        context = {
            'quiz_id': quiz_id,
            'round_id': round.id
        }
        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round.id)


class EditRoundView(LoginRequiredMixin, View):

    def get(self, request, quiz_id, round_id):
        '''
        Render the form to edit a round
        Attributes:
            None
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)
        round_wrapper = get_round_or_404(quiz_wrapper.quiz, round_id)

        context = {
            'quiz': quiz_wrapper.edit_info(),
            'round': round_wrapper.edit_info(),
            'question_types': dict(QuestionType.choices)
        }
        return render(request, 'quiz/create/round.html', context)

    def post(self, request, quiz_id, round_id):
        '''
        Edit the attributes of the round model
        Attributes:
            PARAMS:
                - quiz_id, round_id
            POST:
                - round_info
        ''' 
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)
        round_wrapper = get_round_or_404(quiz_wrapper.quiz, round_id)
        round_info = filter_round_info(request.POST)
        round_wrapper.edit(round_info)
        return redirect('quiz:edit-quiz', quiz_id=quiz_id, round_id=round_id)


class DeleteRoundView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id):
        '''
        Delete a round
        Attributes:
            PARAMS:
                - quiz_id, round_id
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)
        round_wrapper = get_round_or_404(quiz_wrapper.quiz, round_id)

        round_wrapper.round.delete()

        return redirect('quiz:edit-quiz', quiz_id=quiz_id)   