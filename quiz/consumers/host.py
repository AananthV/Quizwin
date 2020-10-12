from asgiref.sync import async_to_sync

from quiz.consumers.base import QuizConsumer
from quiz.classes.quiz import get_quiz
from quiz.classes.round import get_round, get_round_by_id
from quiz.classes.question import get_question, get_question_by_id
from quiz.classes.buzzer import Buzzer
from quiz.classes.participant import Participants
from quiz.constants import RoundType, QuestionType, QuestionClass
from quiz.models import QuizRoom, QuizState

class HostConsumer(QuizConsumer):

    def connect(self):
        '''
        Connect a host to the quiz room
        '''
        # Get user object
        self.user = self.scope['user']
        
        # Disconnect if not authenticated
        if not self.user.is_authenticated:
            return self.close()

        # Get room_id from url
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        # Check if room exists and if user is host
        self.quiz_room = QuizRoom.objects.filter(pk=self.room_id, quiz__host_id=self.user.id)
        if not self.quiz_room.exists():
            return self.close()
        else:
            self.quiz_room = self.quiz_room[0]

        # Get quiz wrapper
        self.quiz = get_quiz(self.quiz_room.quiz)
        self.round = None
        self.question = None
        if self.quiz.state.round is not None:
            self.round = get_round(self.quiz.state.round)
        if self.quiz.state.question is not None:
            self.question = get_question(self.quiz.state.question)

        # Get list of buzzes
        self.buzzer = Buzzer()

        # Get list of participants
        self.participants = Participants(self.quiz_room.quiz_id)

        # Connect to quiz_group
        self.join_room(self.room_id)

        # Accept the connection
        self.accept()

    def receive_json(self, content):
        '''
        Called when we recieve a text frame
        '''
        # Messages will have a "command" key we can switch on
        command = content.get('command', None)

        # Refresh quiz state once
        self.quiz.state.refresh_from_db()

        try:
            if command == 'start':
                self.start_quiz()
            elif command == 'next_round':
                self.next_round()
            elif command == 'next_question':
                self.next_question()
            elif command == 'choose_question':
                self.choose_question(content['question_id'])
            elif command == 'score_question':
                self.score_question(content)
            elif command == 'lock_buzzer':
                self.lock_buzzer()
            elif command == 'unlock_buzzer':
                self.unlock_buzzer()
            elif command == 'reset_buzzer':
                self.reset_buzzer()
            elif command == 'request_ping':
                self.request_ping()
            elif command == 'status':
                self.get_status()
        except Exception as e:
            # Catch any errors and send it back
            self.send_json({"error": e.code})

    # Helpers

    def get_status(self):
        '''
        Get status
        '''
        status = {}

        status['quiz'] = self.quiz.edit_info()
        status['participants'] = self.participants.info()

        if self.round is not None:
            status['round'] = self.round.info()

        if self.question is not None:
            status['question'] = self.question.host_info()

        self.send_json({
            'type': 'status',
            'status': status
        })

    def next_round(self):
        '''
        Move on to the next round
        '''
        if not self.quiz.state.started:
            # TODO: Raise exception
            return
        self.quiz.next_round()
        self.send_round(self.quiz.state.round_id)
        
    def next_question(self):
        '''
        Move on to the next question (SEQUENTIAL Round)
        '''
        if self.quiz.state.round is None or self.quiz.state.round.type != RoundType.SEQUENTIAL:
            # TODO: Raise exception
            print('nope no question')
            return
        self.round.next_question(self.quiz.state)
        self.send_question(self.quiz.state.question_id)
        self.buzzer.reset()
        self.send_buzzer_state()

    def choose_question(self, question_id):
        '''
        Choose the next question (BOARD Round)
        '''
        if not self.quiz.state.round or self.quiz.state.round.type != RoundType.BOARD:
            print(self.quiz.state.round, )
            # TODO: Raise exception
            return
        self.round.choose_question(self.quiz.state, question_id)
        self.send_question(self.quiz.state.question_id)
        self.buzzer.reset()
        self.send_buzzer_state()

    def score_question(self, content):
        '''
        Assign score (NORMAL Question)
        '''
        if self.quiz.state.question is None or self.question.question.type != QuestionType.NORMAL:
            return

        if 'user_id' not in content or 'correct' not in content:
            return
        user_id = content['user_id']
        correct = content['correct']

        if not self.participants.exists(user_id):
            return

        self.question.award_points(user_id, correct)
        self.participants.update_score(user_id)
        self.send_participants()

    def lock_buzzer(self):
        '''
        Lock the buzzer
        '''
        if not self.buzzer.locked:
            self.buzzer.lock()
            self.send_buzzer_state()

    def unlock_buzzer(self):
        '''
        Unlock the buzzer
        '''
        if self.buzzer.locked:
            self.buzzer.unlock()
            self.send_buzzer_state()

    def reset_buzzer(self):
        '''
        Reset the buzzer
        '''
        self.buzzer.reset()
        self.send_buzzer_state()

    # Event Dispatchers

    # Ping

    def request_ping(self):
        '''
        Request a ping from connected participants
        '''
        self.broadcast({
            'type': 'ping.request'
        })

    # Room

    def accept_user(self, user_id):
        '''
        Accept a user
        '''
        self.participants.add_user(user_id)
        self.broadcast({
            'type': 'room.accept',
            'user_id': user_id
        })

    def reject_user(self, channel_name):
        '''
        Reject a user
        '''
        self.transmit(channel_name, {
            'type': 'room.reject'
        })

    # Quiz

    def start_quiz(self):
        '''
        Start the quiz
        '''
        if self.quiz.state.started:
            # TODO: Return exception
            return
        self.quiz.state.started = True
        self.quiz.state.save()

        self.broadcast({
            'type': 'quiz.start'
        })

    def send_round(self, round_id):
        '''
        Send the round_id to the room
        '''
        self.broadcast({
            'type': 'quiz.round',
            'round_id': round_id
        })

    def send_question(self, question_id):
        '''
        Send the question_id to the room
        '''
        self.broadcast({
            'type': 'quiz.question',
            'question_id': question_id
        })

    # Buzzer

    def send_buzzer_state(self):
        '''
        Send the buzzer state to the room
        '''
        self.broadcast({
            'type': 'buzzer.info',
            'info': self.buzzer.state()
        })

    def send_participants(self):
        self.send_json({
            'type': 'quiz.participants',
            'info': self.participants.info()
        })

    # Event Receivers

    # Ping

    def ping_ping(self, event):
        '''
        Called when we receive a ping
        '''
        if not self.participants.exists(event['user_id']):
            self.participants.add_user(event['user_id'])
            print(self.participants.participants)

    # Room

    def room_join(self, event):
        user_id = event['user_id']

        # If host second screen
        if user_id == self.user.id:
            return

        if self.participants.exists(user_id):
            self.reject_user(event['channel_name'])
        else:
            self.accept_user(user_id)

    def room_leave(self, event):
        user_id = event['user_id']
        if self.participants.exists(user_id):
            self.participants.remove_user(user_id)

            if user_id in self.buzzer.buzzes:
                self.buzzer.buzzes.remove(user_id)

            self.send_participants()
            self.send_json({
                'type': 'room.leave',
                'user_id': user_id
            })

    def room_accept(self, event):
        super().room_accept(event)
        self.send_participants()

    # Buzzer

    def buzzer_buzz(self, event):
        '''
        Called when a participant buzzes
        '''
        user_id = event['user_id']
        if not self.buzzer.locked and not self.buzzer.buzzed(user_id) and self.participants.exists(user_id):
            self.buzzer.buzz(user_id)
            self.send_buzzer_state()

    # Quiz

    def quiz_round(self, event):
        '''
        Called when we receive the next round
        '''
        self.round = get_round_by_id(event['round_id'])
        self.send_json({
            'type': 'quiz.round',
            'info': self.round.info()
        })

    def quiz_question(self, event):
        self.question = get_question_by_id(event['question_id'])
        self.buzzer.reset()

        self.send_json({
            'type': 'quiz.question',
            'info': self.question.host_info()
        })

    def quiz_answer(self, event):
        '''
        Called when we receive an answer
        '''
        user_id = event['user_id']
        answer = event['answer']
        if self.question.question_class == QuestionClass.CHOICE_ANSWER and not self.buzzer.locked and not self.buzzer.buzzed(user_id) and self.participants.exists(user_id):
            self.question.award_points(user_id, answer)
            self.participants.update_score(user_id)
            self.buzzer.answer(user_id, answer)
            self.send_participants()
            self.send_buzzer_state()