from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.models import Quiz
from quiz.classes.quiz import create_quiz, get_quiz_or_404, filter_quiz_info
from quiz.constants import RoundType


class CreateQuizView(LoginRequiredMixin, View):
    
    def post(self, request):
        '''
        Create a quiz
        Attributes:
            none.
        '''
        quiz = create_quiz(request.user)
        return redirect('quiz:edit-quiz', quiz_id=quiz.id)


class EditQuizView(LoginRequiredMixin, View):

    def get(self, request, quiz_id):
        '''
        Render the form to edit a quiz
        Attributes:
            None
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)

        context = {
            'quiz': quiz_wrapper.edit_info(),
            'round_types': dict(RoundType.choices)
        }
        # return context
        return render(request, 'quiz/create/quiz.html', context)

    def post(self, request, quiz_id):
        '''
        Edit the attributes of the quiz model
        Attributes:
            PARAMS:
                - quiz_id
            POST:
                - quiz_info
        ''' 
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)
        
        quiz_info = filter_quiz_info(request.POST)

        quiz_wrapper.edit(quiz_info)
        
        return redirect('quiz:edit-quiz', quiz_id=quiz_id)


class DeleteQuizView(LoginRequiredMixin, View):

    def post(self, request, quiz_id):
        '''
        Delete a quiz
        Attributes:
            PARAMS:
                - quiz_id
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)

        quiz_wrapper.quiz.delete()

        # TODO: Have some kinda notification in dashboard, "successfully deleted" etc
        return redirect('quiz:profile') 