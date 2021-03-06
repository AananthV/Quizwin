from django.views import View
from django.shortcuts import redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.question import get_question_or_404
from quiz.constants import SlideType

class CreateSlideView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id):
        '''
        Create a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
            POST:
                - type
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        question_wrapper.create_slide(request.POST.copy())

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class EditSlideView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, slide_id):
        '''
        Edit a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
            POST:
                - slide_info
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        slide_info = request.POST.get('info', '')

        question_wrapper.edit_slide(slide_id, slide_info)

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)

class DeleteSlideView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, question_id, slide_id):
        '''
        Edit a slide
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - question_id
        '''
        question_wrapper = get_question_or_404(request.user, quiz_id, round_id, question_id)

        question_wrapper.delete_slide(slide_id)

        return redirect('quiz:edit-question', quiz_id=quiz_id, round_id=round_id, question_id=question_id)