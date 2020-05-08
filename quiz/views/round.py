from django.views import View
from django.shortcuts import render, redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.round import create_round_or_404, get_round_or_404, filter_round_info
from quiz.classes.quiz import get_quiz_or_404
from quiz.constants import QuestionType, RoundType

class CreateRoundView(LoginRequiredMixin, View):
    
    def post(self, request, quiz_id):
        '''
        Create a round
        Attributes:
            body containing round_info
        '''
        round_info = {
            'type': request.POST.get('type')
        }

        round = create_round_or_404(request.user, quiz_id, round_info)

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round.id)


class EditRoundView(LoginRequiredMixin, View):

    def get(self, request, quiz_id, round_id):
        '''
        Render the form to edit a round
        Attributes:
            None
        '''
        round_wrapper = get_round_or_404(request.user, quiz_id, round_id)

        context = {
            'quiz_id': quiz_id,
            'round_id': round_id,
            'round': round_wrapper.edit_info(),
            'question_types': dict(QuestionType.choices),
            'RoundType': RoundType
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
        round_wrapper = get_round_or_404(request.user, quiz_id, round_id)

        round_info = filter_round_info(request.POST.copy())

        round_wrapper.edit(round_info)

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round_id)


class DeleteRoundView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id):
        '''
        Delete a round
        Attributes:
            PARAMS:
                - quiz_id, round_id
        '''
        round_wrapper = get_round_or_404(request.user, quiz_id, round_id)

        round_wrapper.delete()

        return redirect('quiz:edit-quiz', quiz_id=quiz_id)   