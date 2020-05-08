from django.views import View
from django.shortcuts import redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.question import get_question_or_404
from quiz.constants import QuestionType, SlideType

class CreateAnswerView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id):
        '''
        Create a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
            POST:
                - answer_info depending on question type
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        question_wrapper.set_answer(request.POST.copy())

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class EditAnswerView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, answer_id):
        '''
        Edit answer
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
                - answer_id (unused)
            POST:
                - answer_info
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        if question_wrapper.question.type == QuestionType.NORMAL:
            question_wrapper.edit_answer(request.POST.copy())
        else:
            # TODO: Return exception
            pass

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class DeleteAnswerView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, answer_id):
        '''
        Edit a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
                - answer_id (unused)
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        if question_wrapper.question.type == QuestionType.NORMAL:
            question_wrapper.delete_answer()
        else:
            # TODO: Return exception
            pass

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)