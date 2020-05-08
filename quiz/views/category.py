from django.views import View
from django.shortcuts import redirect

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.classes.round import get_category_round_or_404

class CreateCategoryView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id):
        '''
        Add a category to a round
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
        '''
        round_wrapper = get_category_round_or_404(request.user, quiz_id, round_id)
        
        name = request.POST.get('name', 'Untitled')

        round_wrapper.add_category(name)

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round_id)

class EditCategoryView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, category_id):
        '''
        Rename a caegory
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - category_id
        '''
        round_wrapper = get_category_round_or_404(request.user, quiz_id, round_id)
        
        name = request.POST.get('name', 'Untitled')

        round_wrapper.rename_category(category_id, name)

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round_id)
    
class DeleteCategoryView(LoginRequiredMixin, View):

    def post(self, request, quiz_id, round_id, category_id):
        '''
        Delete a caegory
        Attributes:
            PARAMS:
                - quiz_id
                - round_id
                - category_id
        '''
        round_wrapper = get_category_round_or_404(request.user, quiz_id, round_id)

        round_wrapper.delete_category(category_id)

        return redirect('quiz:edit-round', quiz_id=quiz_id, round_id=round_id)