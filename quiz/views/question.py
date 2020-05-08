from django.views import View
from django.shortcuts import render, redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.question import create_question_or_404, filter_question_info, get_question_or_404
from quiz.constants import QuestionClass, QuestionType, SlideType

class CreateQuestionView(LoginRequiredMixin, View):
    
    def post(self, request, quiz_id, round_id):
        '''
        Create a question
        Attributes:
            none.
        '''
        question_info = filter_question_info(request.POST.copy())
        question = create_question_or_404(request.user, quiz_id, round_id, question_info)

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question.id)

class EditQuestionView(LoginRequiredMixin, View):

    def get(self, request, quiz_id, round_id, question_id):
        '''
        Render the form to edit a question
        Attributes:
            None
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)
        context = {
            'quiz_id': quiz_id,
            'round_id': round_id,
            'question_id': question_id,
            'question': question_wrapper.host_info(),
            'question_types': dict(QuestionType.choices),
            'slide_types': dict(SlideType.choices),
            'QuestionClass': QuestionClass,
            'QuestionType': QuestionType,
            'SlideType': SlideType,
        }
        # print(context)
        # return context
        return render(request, 'quiz/create/question.html', context)

    def post(self, request, quiz_id, round_id, question_id):
        '''
        Edit the attributes of the question model
        Attributes:
            PARAMS:
                - quiz_id, round_id, question_id
            POST:
                - question_info
        ''' 
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        question_info = filter_question_info(request.POST.copy())

        question_wrapper.edit(question_info)

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class DeleteQuestionView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id):
        '''
        Delete a question
        Attributes:
            PARAMS:
                - quiz_id, round_id, question_id
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        question_wrapper.delete()

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round_id)