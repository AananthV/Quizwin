from django.views import View
from django.shortcuts import redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.question import get_question_or_404
from quiz.constants import QuestionType, SlideType, QuestionClass

class CreateChoiceView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id):
        '''
        Create a choice
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
            POST:
                - choice_info
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        if not question_wrapper.question_class == QuestionClass.CHOICE_ANSWER:
            # TODO: Return exception
            pass
        
        question_wrapper.add_choice(request.POST.copy())

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class EditChoiceView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, choice_id):
        '''
        Edit answer
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
                - choice_id
            POST:
                - choice_info
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        if not question_wrapper.question_class == QuestionClass.CHOICE_ANSWER:
            # TODO: Return exception
            pass

        question_wrapper.edit_choice(choice_id, request.POST.copy())

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class DeleteChoiceView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, choice_id):
        '''
        Edit a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
                - choice_id
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        if not question_wrapper.question_class == QuestionClass.CHOICE_ANSWER:
            # TODO: Return exception
            pass

        question_wrapper.delete_choice(choice_id)

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)