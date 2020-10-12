from django.views import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from quiz.mixins.requires_login import LoginRequiredMixin
from quiz.models import QuizRoom, QuizParticipant

class JoinView(LoginRequiredMixin, View):

    def get(self, request):
        '''
        Render form for joining a quiz
        '''
        return render(request, 'quiz/play/index.html')

    def post(self, request):
        '''
        Join a quiz
        Attributes:
            POST:
                - room_id
                - quiz_secret
        '''
        try:
            room_id = request.POST.get('room_id')
            quiz_secret = request.POST.get('quiz_secret')
        except Exception as e:
            # TODO: Return Exception
            return {}

        room = get_object_or_404(QuizRoom, pk=room_id, quiz__secret=quiz_secret)

        QuizParticipant.objects.get_or_create(room_id=room.id, user_id=request.user.id)

        return redirect('quiz:participate', room_id=room_id)

class ParticipateView(LoginRequiredMixin, View):
    
    def get(self, request, room_id):
        '''
        Render participate page
        '''
        context = {
            'room_id': room_id
        }
        return render(request, 'quiz/play/participate.html', context)