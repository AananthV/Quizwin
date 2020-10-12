from asgiref.sync import async_to_sync

from quiz.classes.quiz import get_quiz
from quiz.classes.round import get_round, get_round_by_id
from quiz.classes.question import get_question, get_question_by_id
from quiz.consumers.base import QuizConsumer
from quiz.models import QuizParticipant, QuizRoom

class ParticipantConsumer(QuizConsumer):

    def connect(self):
        '''
        Conenct participant to quiz room
        '''
        # Get user object
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return self.close()

        # Get room_id, check if user has access to room_id
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        if not QuizParticipant.objects.filter(room_id=self.room_id, user_id=self.user.id).exists():
            return self.close()

        self.quiz_room = QuizRoom.objects.get(pk=self.room_id)

        self.quiz = get_quiz(self.quiz_room.quiz)
        self.round = None
        self.question = None
        if self.quiz.state.round is not None:
            self.round = get_round(self.quiz.state.round)
        if self.quiz.state.question is not None:
            self.question = get_question(self.quiz.state.question)

        # Connect to quiz room
        self.join_room(self.room_id)

        # Accept the connection
        self.accept()

    def receive_json(self, content):
        '''
        Called when we recieve a text frame
        '''
        # Messages will have a "command" key we can switch on
        command = content.get('command', None)

        try:
            if command == 'status':
                self.get_status()
            elif command == 'buzz':
                self.send_buzz()
            elif command == 'answer':
                self.send_answer(content['answer'])
        except Exception as e:
            # Catch any errors and send it back
            self.send_json({"error": e})

    # Helpers
    def get_status(self):
        '''
        Get status
        '''
        status = {}

        status['quiz'] = self.quiz.info()

        if self.round is not None:
            status['round'] = self.round.info()

        if self.question is not None:
            status['question'] = self.question.player_info()

        self.send_json({
            'type': 'status',
            'status': status
        })

    # Event Dispatchers

    def send_buzz(self):
        self.broadcast({
            'type': 'buzzer.buzz',
            'user_id': self.user.id
        })

    def send_answer(self, answer):
        self.broadcast({
            'type': 'quiz.answer',
            'user_id': self.user.id,
            'answer': answer
        })

    # Event Receivers

    # Ping

    def ping_request(self, event):
        self.broadcast({
            'type': 'ping.ping',
            'user_id': self.user.id
        })

    # Buzzer

    def buzzer_info(self, event):
        '''
        Triggered when host sends buzzer update
        '''
        filtered_event = {
            'type': event['type'],
            'info': event['info'].copy()
        }
        del filtered_event['info']['answers']

        super().buzzer_info(filtered_event)

    # Quiz

    def quiz_round(self, event):
        self.round = get_round_by_id(event['round_id'])
        self.send_json({
            'type': 'quiz.round',
            'info': self.round.base_info()
        })

    def quiz_question(self, event):
        self.question = get_question_by_id(event['question_id'])
        self.send_json({
            'type': 'quiz.question',
            'info': self.question.player_info()
        })