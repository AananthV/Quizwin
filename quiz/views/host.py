from django.views import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from quiz.classes.quiz import get_quiz_or_404
from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.models import QuizRoom

class StartQuizView(LoginRequiredMixin, View):
    def post(self, request, quiz_id):
        '''
        Start a quiz
        '''
        quiz_wrapper = get_quiz_or_404(request.user, quiz_id)

        # TODO: Check if quiz is valid

        quiz_room, created = QuizRoom.objects.get_or_create(quiz_id=quiz_id)

        return redirect('quiz:host', room_id=quiz_room.id)

class HostView(LoginRequiredMixin, View):

    def get(self, request, room_id):
        '''
        Render host page
        '''
        context = {
            'room_id': room_id
        }
        return render(request, 'quiz/play/host.html', context)