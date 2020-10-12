from django.urls import path

from quiz.consumers import participant, host

websocket_urlpatterns = [
    path('ws/host/<int:room_id>/', host.HostConsumer),
    path('ws/participate/<int:room_id>/', participant.ParticipantConsumer),
]